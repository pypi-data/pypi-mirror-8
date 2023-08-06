# -*- coding: utf-8 -*-

from __future__ import absolute_import

import collections
import datetime
import logging
import random
import uuid

from blinker import signal

from ._compat import urlparse, text_types


def mysql_pub(mysql_dsn, tables=None, blocking=False, **kwargs):
    """MySQL row-based binlog events publisher.

    The additional kwargs will be passed to `BinLogStreamReader`.
    """
    # only import when used to avoid dependency requirements
    import pymysqlreplication
    from pymysqlreplication.row_event import (
        DeleteRowsEvent,
        UpdateRowsEvent,
        WriteRowsEvent,
    )

    logger = logging.getLogger("meepo.pub.mysql_pub")

    # parse mysql settings
    parsed = urlparse(mysql_dsn)
    mysql_settings = {
        "host": parsed.hostname,
        "port": parsed.port or 3306,
        "user": parsed.username,
        "passwd": parsed.password
    }

    # connect to binlog stream
    stream = pymysqlreplication.BinLogStreamReader(
        mysql_settings,
        server_id=random.randint(1000000000, 4294967295),
        blocking=blocking,
        only_events=[DeleteRowsEvent, UpdateRowsEvent, WriteRowsEvent],
        **kwargs
    )

    def _pk(values):
        if isinstance(event.primary_key, text_types):
            return values[event.primary_key]
        return tuple(values[k] for k in event.primary_key)

    for event in stream:
        if not event.primary_key:
            continue

        if tables and event.table not in tables:
            continue

        try:
            rows = event.rows
        except (UnicodeDecodeError, ValueError) as e:
            logger.exception(e)
            continue

        timestamp = datetime.datetime.fromtimestamp(event.timestamp)

        if isinstance(event, WriteRowsEvent):
            sg_name = "{}_write".format(event.table)
            sg = signal(sg_name)
            sg_raw = signal("{}_raw".format(sg_name))

            for row in rows:
                pk = _pk(row["values"])
                sg.send(pk)
                sg_raw.send(row)

                logger.debug("{} -> {}, {}".format(sg_name, pk, timestamp))

        elif isinstance(event, UpdateRowsEvent):
            sg_name = "{}_update".format(event.table)
            sg = signal(sg_name)
            sg_raw = signal("{}_raw".format(sg_name))

            for row in rows:
                pk = _pk(row["after_values"])
                sg.send(pk)
                sg_raw.send(row)

                logger.debug("{} -> {}, {}".format(sg_name, pk, timestamp))

        elif isinstance(event, DeleteRowsEvent):
            sg_name = "{}_delete".format(event.table)
            sg = signal(sg_name)
            sg_raw = signal("{}_raw".format(sg_name))

            for row in rows:
                pk = _pk(row["values"])
                sg.send(pk)
                sg_raw.send(row)

                logger.debug("{} -> {}, {}".format(sg_name, pk, timestamp))

        signal("mysql_binlog_pos").send("{}:{}".format(stream.log_file,
                                                       stream.log_pos))


def sqlalchemy_pub(dbsession, strict_tables=None):
    """SQLAlchemy events publisher.

    This publisher don't publish events itself, it will hook on sqlalchemy's
    event system, and publish the changes automatically.

    When `strict_tables` provided, two more signals may be triggered for table
    included. They can be used with prepare-commit pattern to help ensure 100%
    reliability on event sourcing (and broadcasting), note this will
    need another monitor daemon to monitor the status. For more info about
    this patter, refer to documentation.
    """
    from sqlalchemy import event

    logger = logging.getLogger("meepo.pub.sqlalchemy_pub")

    def _pk(obj):
        """Get pk values from object
        """
        pk_values = tuple(getattr(obj, c.name)
                          for c in obj.__mapper__.primary_key)
        if len(pk_values) == 1:
            return pk_values[0]
        return pk_values

    def _pub(obj, action):
        """Publish object pk values with action.
        """
        sg_name = "{}_{}".format(obj.__table__, action)
        sg = signal(sg_name)
        sg_raw = signal("{}_raw".format(sg_name))

        pk = _pk(obj)
        if pk:
            logger.debug("{} -> {}".format(sg_name, pk))
            sg.send(pk)
            sg_raw.send(obj)

    def session_init(session, *args, **kwargs):
        if hasattr(session, "meepo_unique_id"):
            logger.debug("skipped - session_init")
            return

        for action in ("write", "update", "delete"):
            attr = "pending_{}".format(action)
            if not hasattr(session, attr):
                setattr(session, attr, set())
        session.meepo_unique_id = uuid.uuid4().hex
        logger.debug("%s - session_init" % session.meepo_unique_id)

    def session_del(session):
        del session.meepo_unique_id
        del session.pending_write
        del session.pending_update
        del session.pending_delete

    def before_flush_hook(session, flush_ctx, nonsense):
        """Record session changes on flush
        """
        session_init(session)
        logger.debug("%s - before_flush" % session.meepo_unique_id)
        session.pending_write |= set(session.new)
        session.pending_update |= set(session.dirty)
        session.pending_delete |= set(session.deleted)
    event.listen(dbsession, "before_flush", before_flush_hook)

    def _pub_session(session):
        logger.debug("pub_session")
        for obj in session.pending_write:
            _pub(obj, action="write")
        for obj in session.pending_update:
            _pub(obj, action="update")
        for obj in session.pending_delete:
            _pub(obj, action="delete")

        session.pending_write.clear()
        session.pending_update.clear()
        session.pending_delete.clear()

    if not strict_tables:
        def after_commit_hook(session):
            """Publish signals
            """
            _pub_session(session)
            session_del(session)
        event.listen(dbsession, "after_commit", after_commit_hook)

    else:
        logger.debug("strict_tables: {}".format(strict_tables))

        def session_prepare(session, flush_ctx):
            """Record session prepare state in before_commit
            """
            if not hasattr(session, 'meepo_unique_id'):
                session_init(session)

            logger.debug("%s - after_flush" % session.meepo_unique_id)

            for action in ("write", "update", "delete"):
                objs = [o for o in getattr(session, "pending_%s" % action)
                        if o.__table__.fullname in strict_tables]
                if not objs:
                    continue

                prepare_event = collections.defaultdict(set)
                for obj in objs:
                    prepare_event[obj.__table__.fullname].add(_pk(obj))
                logger.debug("{} - session_prepare_{} -> {}".format(
                    session.meepo_unique_id, action, prepare_event))
                signal("session_prepare").send(
                    prepare_event, sid=session.meepo_unique_id, action=action)
        event.listen(dbsession, "after_flush", session_prepare)

        def session_commit(session):
            """Commit session in after_commit
            """
            # this may happen when there's nothing to commit
            if not hasattr(session, 'meepo_unique_id'):
                logger.debug("skipped - after_commit")
                return

            # normal session pub
            logger.debug("%s - after_commit" % session.meepo_unique_id)
            _pub_session(session)
            signal("session_commit").send(session.meepo_unique_id)
            session_del(session)
        event.listen(dbsession, "after_commit", session_commit)

        def session_rollback(session):
            """Clean session in after_rollback.
            """
            # this may happen when there's nothing to rollback
            if not hasattr(session, 'meepo_unique_id'):
                logger.debug("skipped - after_rollback")
                return

            # del session meepo id after rollback
            logger.debug("%s - after_rollback" % session.meepo_unique_id)
            signal("session_rollback").send(session.meepo_unique_id)
            session_del(session)
        event.listen(dbsession, "after_rollback", session_rollback)
