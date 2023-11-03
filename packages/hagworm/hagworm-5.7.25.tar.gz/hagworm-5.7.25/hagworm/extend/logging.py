# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import os
import sys
import signal
import queue
import logging

from abc import ABCMeta, abstractmethod
from datetime import timedelta

from loguru._file_sink import FileSink

from elasticsearch import Elasticsearch, ApiError as ESApiError, NotFoundError as ESNotFoundError, helpers as es_helpers
from confluent_kafka import Producer as KFKProducer

from .trace import get_trace_id
from .base import Utils
from .asyncio.future import Thread


class LogFileRotator:

    @classmethod
    def make(cls, _size=500, _time=r'00:00'):

        return cls(_size, _time).should_rotate

    def __init__(self, _size, _time):

        _size = _size * (1024 ** 2)
        _time = Utils.split_int(_time, r':')

        now_time = Utils.today()

        self._size_limit = _size
        self._time_limit = now_time.replace(hour=_time[0], minute=_time[1])

        if now_time >= self._time_limit:
            self._time_limit += timedelta(days=1)

    def should_rotate(self, message, file):

        file.seek(0, 2)

        if file.tell() + len(message) > self._size_limit:
            return True

        if message.record[r'time'].timestamp() > self._time_limit.timestamp():
            self._time_limit += timedelta(days=1)
            return True

        return False


DEFAULT_LOG_FILE_ROTATOR = LogFileRotator.make()


class InterceptHandler(logging.Handler):
    """日志拦截器
    """

    def emit(self, record):

        Utils.log.opt(
            depth=8,
            exception=record.exc_info
        ).log(
            record.levelname,
            record.getMessage()
        )


class _BaseSink(metaclass=ABCMeta):
    """基础日志投递基类
    """

    def __init__(self, buffer_maxsize: int = 0xffff, bulk_maxsize: int = 0x800, write_max_delay: int = 5):

        self._buffer = queue.Queue(buffer_maxsize)

        self._bulk_maxsize = bulk_maxsize
        self._write_max_delay = write_max_delay

        self._task = Thread(target=self._do_task)
        self._task.start()

        signal.signal(signal.SIGINT, self.close)
        signal.signal(signal.SIGTERM, self.close)

    def write(self, message):

        try:

            if message.record[r'thread'].id == self._task.ident or not message.record[r'message'].strip():
                return

            log_extra = message.record[r'extra']

            if r'trace_id' not in log_extra:

                trace_id = get_trace_id()

                if trace_id is not None:
                    log_extra[r'trace_id'] = trace_id

            self._buffer.put_nowait(message)

        except queue.Full as _:

            if message.record[r'level'].no > logging.INFO:
                sys.stderr.write(str(message))

        except Exception as err:

            sys.stderr.write(f'{str(err)}\n')

    def close(self, *_):

        self._task.wait(10)

    def _do_task(self):

        messages = []

        while True:

            try:

                for _idx in range(self._write_max_delay):

                    try:

                        messages.append(
                            self._buffer.get(block=True, timeout=1)
                        )

                        self._buffer.task_done()

                    except queue.Empty:

                        pass

                    finally:

                        if len(messages) >= self._bulk_maxsize or (_idx + 1) >= self._write_max_delay:
                            break

                if messages:
                    self._write_logs(messages)
                    messages.clear()

            except Exception as err:

                sys.stderr.write(f'{str(err)}\n')

    @abstractmethod
    def _write_logs(self, logs):

        raise NotImplementedError()


class QueuedFileSink(_BaseSink, FileSink):
    """日志文件队列
    """

    def __init__(
            self, path, *,
            buffer_maxsize: int = 0xffff, bulk_maxsize: int = 0x800, write_max_delay: int = 5,
            **kwargs
    ):

        _BaseSink.__init__(self, buffer_maxsize, bulk_maxsize, write_max_delay)
        FileSink.__init__(self, path, **kwargs)

    def _write_logs(self, logs):

        for _log in logs:
            FileSink.write(self, _log)


class KafkaSink(_BaseSink):
    """Kafka日志投递
    """

    def __init__(
            self, servers, topic, *,
            buffer_maxsize: int = 0xffff, bulk_maxsize: int = 0x800, write_max_delay: int = 5,
            **kwargs
    ):

        super().__init__(buffer_maxsize, bulk_maxsize, write_max_delay)

        kwargs[r'bootstrap.servers'] = servers

        self._producer = KFKProducer(kwargs)

        self._topic = topic

    def _write_logs(self, logs):

        for _log in logs:
            self._producer.produce(
                self._topic,
                Utils.json_encode(
                    {
                        r'extra': _log.record[r'extra'],
                        r'process': {
                            r'id': _log.record[r'process'].id,
                            r'name': _log.record[r'process'].name,
                        },
                        r'thread': {
                            r'id': _log.record[r'thread'].id,
                            r'name': _log.record[r'thread'].name,
                        },
                        r'level': {
                            r'no': _log.record[r'level'].no,
                            r'name': _log.record[r'level'].name,
                        },
                        r'module': f"{_log.record[r'name']}:{_log.record[r'function']}:{_log.record[r'line']}",
                        r'message': _log.record[r'message'],
                        r'timestamp': int(_log.record[r'time'].timestamp() * 1000),
                    }
                ),
            )

            self._producer.poll(0)

        self._producer.flush()


class ElasticsearchDataStreamUtil:

    def __init__(
            self, elasticsearch: Elasticsearch, stream_name: str, *,
            rollover_max_age: str = r'1d', rollover_max_primary_shard_size: str = r'50gb', delete_min_age: str = r'30d',
            refresh_interval: str = r'5s', number_of_replicas=0, timestamp_order: str = r'desc'
    ):

        self._elasticsearch = elasticsearch

        self._stream_name = stream_name
        self._policy_name = f'{stream_name}-ilm-policy'

        self._rollover_max_age = rollover_max_age
        self._rollover_max_primary_shard_size = rollover_max_primary_shard_size

        self._delete_min_age = delete_min_age
        self._refresh_interval = refresh_interval
        self._number_of_replicas = number_of_replicas
        self._timestamp_order = timestamp_order

    def initialize(self):

        try:
            self._elasticsearch.indices.get_data_stream(name=self._stream_name)
        except ESNotFoundError as _:
            self._create_lifecycle()
            self._create_index_template()
        except ESApiError as err:
            sys.stderr.write(f'{str(err.info)}\n')
        except Exception as err:
            sys.stderr.write(f'{str(err)}\n')

    def _create_lifecycle(self):

        try:

            policy = {
                r'phases': {
                    r'hot': {
                        r'actions': {
                            r'rollover': {
                                r'max_age': self._rollover_max_age,
                                r'max_primary_shard_size': self._rollover_max_primary_shard_size,
                            },
                            r'set_priority': {
                                r'priority': 100,
                            }
                        },
                        r'min_age': r'0ms',
                    },
                    r'delete': {
                        r'actions': {
                            r'delete': {}
                        },
                        r'min_age': self._delete_min_age,
                    },
                },
            }

            self._elasticsearch.ilm.put_lifecycle(name=self._policy_name, policy=policy)

        except ESApiError as err:

            sys.stderr.write(f'{str(err.info)}\n')

        except Exception as err:

            sys.stderr.write(f'{str(err)}\n')

    def _create_index_template(self):

        try:

            mappings = {
                r'dynamic': r'strict',
                r'properties': {
                    r'extra': {
                        r'type': r'flattened',
                    },
                    r'process': {
                        r'properties': {
                            r'id': {
                                r'type': r'keyword',
                            },
                            r'name': {
                                r'type': r'keyword',
                                r'ignore_above': 64,
                            },
                        },
                    },
                    r'thread': {
                        r'properties': {
                            r'id': {
                                r'type': r'keyword',
                            },
                            r'name': {
                                r'type': r'keyword',
                                r'ignore_above': 64,
                            },
                        },
                    },
                    r'level': {
                        r'properties': {
                            r'no': {
                                r'type': r'integer',
                            },
                            r'name': {
                                r'type': r'keyword',
                                r'ignore_above': 64,
                            },
                        },
                    },
                    r'module': {
                        r'type': r'text',
                        r'norms': False,
                    },
                    r'message': {
                        r'type': r'text',
                        r'norms': False,
                    },
                    r'@timestamp': {
                        r'type': r'date',
                    },
                }
            }

            template = {
                r'settings': {
                    r'index': {
                        r'lifecycle': {
                            r'name': self._policy_name,
                        },
                        r'refresh_interval': self._refresh_interval,
                        r'number_of_replicas': self._number_of_replicas,
                        r'sort': {
                            r'field': r'@timestamp',
                            r'order': self._timestamp_order,
                        }
                    },
                },
                r'mappings': mappings,
            }

            self._elasticsearch.indices.put_index_template(
                name=self._stream_name,
                template=template,
                index_patterns=[f'{self._stream_name}*'],
                data_stream={},
            )

        except ESApiError as err:

            sys.stderr.write(f'{str(err.info)}\n')

        except Exception as err:

            sys.stderr.write(f'{str(err)}\n')


class ElasticsearchSink(_BaseSink):
    """Elasticsearch日志投递
    """

    def __init__(
            self, hosts, index, *,
            buffer_maxsize: int = 0xffff, bulk_maxsize: int = 0x800, write_max_delay: int = 5,
            rollover_max_age: str = r'1d', rollover_max_primary_shard_size: str = r'50gb', delete_min_age: str = r'30d',
            refresh_interval: str = r'5s', number_of_replicas=0, timestamp_order: str = r'desc',
            **kwargs):

        super().__init__(buffer_maxsize, bulk_maxsize, write_max_delay)

        self._elasticsearch = Elasticsearch(hosts, **kwargs)

        ElasticsearchDataStreamUtil(
            self._elasticsearch, index,
            rollover_max_age=rollover_max_age,
            rollover_max_primary_shard_size=rollover_max_primary_shard_size,
            delete_min_age=delete_min_age,
            refresh_interval=refresh_interval,
            number_of_replicas=number_of_replicas,
            timestamp_order=timestamp_order
        ).initialize()

        self._index = index

    def _write_logs(self, logs):

        es_helpers.bulk(
            self._elasticsearch,
            actions=[
                {
                    r'_op_type': r'create',
                    r'_index': self._index,
                    r'extra': _log.record[r'extra'],
                    r'process': {
                        r'id': _log.record[r'process'].id,
                        r'name': _log.record[r'process'].name,
                    },
                    r'thread': {
                        r'id': _log.record[r'thread'].id,
                        r'name': _log.record[r'thread'].name,
                    },
                    r'level': {
                        r'no': _log.record[r'level'].no,
                        r'name': _log.record[r'level'].name,
                    },
                    r'module': f"{_log.record[r'name']}:{_log.record[r'function']}:{_log.record[r'line']}",
                    r'message': _log.record[r'message'],
                    r'@timestamp': int(_log.record[r'time'].timestamp() * 1000),
                }
                for _log in logs
            ]
        )


DEFAULT_LOG_FILE_NAME = r'runtime_{time}.log'


def init_logger(
        level, *, handler=None,
        file_path=None, file_name=DEFAULT_LOG_FILE_NAME,
        file_rotation=DEFAULT_LOG_FILE_ROTATOR, file_retention=0xff,
        extra=None, enqueue=False, debug=False
):

    level = level.upper()

    Utils.log.remove()

    if extra is not None:

        extra = {_key: _val for _key, _val in extra.items() if _val is not None}

        if extra:
            Utils.log.configure(extra=extra)

    if handler or file_path:

        if handler:
            Utils.log.add(
                handler,
                level=level,
                enqueue=enqueue,
                backtrace=debug
            )

        if file_path:

            _file_name, _file_ext_name = os.path.splitext(file_name)

            Utils.log.add(
                QueuedFileSink(
                    Utils.path.join(file_path, _file_name + '.pid-' + str(Utils.getpid()) + _file_ext_name),
                    rotation=file_rotation,
                    retention=file_retention
                ),
                level=level,
                enqueue=enqueue,
                backtrace=debug
            )

    else:

        Utils.log.add(
            sys.stderr,
            level=level,
            enqueue=enqueue,
            backtrace=debug
        )

    logger = logging.getLogger()
    logger.setLevel(level)
    logger.addHandler(InterceptHandler())
