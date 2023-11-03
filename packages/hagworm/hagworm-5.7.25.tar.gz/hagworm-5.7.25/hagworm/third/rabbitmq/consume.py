# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import typing
import aio_pika

from ...extend.error import catch_error
from ...extend.asyncio.base import Utils


class RabbitMQConsumer:
    """RabbitMQ消费者
    """

    def __init__(self, connection: aio_pika.abc.AbstractRobustConnection, queue_name: str):

        self._connection: aio_pika.abc.AbstractRobustConnection = connection
        self._channel: typing.Optional[aio_pika.abc.AbstractRobustChannel] = None

        self._queue: typing.Optional[aio_pika.abc.AbstractRobustQueue] = None
        self._queue_name: str = queue_name

    @property
    def channel(self) -> aio_pika.abc.AbstractRobustChannel:
        return self._channel

    @property
    def queue(self) -> aio_pika.abc.AbstractRobustQueue:
        return self._queue

    @property
    def queue_name(self) -> str:
        return self._queue_name

    async def open(
            self, *,
            consume_func=None, consume_no_ack=False, channel_qos_config=None, queue_config=None
    ):

        await self._connection.ready()

        if channel_qos_config is None:
            channel_qos_config = {r'prefetch_count': 1}
        elif r'prefetch_count' not in channel_qos_config:
            channel_qos_config[r'prefetch_count'] = 1

        if queue_config is None:
            queue_config = {}

        self._channel = await self._connection.channel()

        await self._channel.set_qos(**channel_qos_config)

        self._queue = await self._channel.declare_queue(self._queue_name, **queue_config)

        if consume_func is not None:
            await self._queue.consume(consume_func, no_ack=consume_no_ack)

        Utils.log.info(f"rabbitmq consumer {self._queue_name} initialized: {channel_qos_config[r'prefetch_count']}")

    async def close(self, with_connection=False):

        await self._channel.close()

        if with_connection is True:
            await self._connection.close()

    async def block_pull(self, consume_func, consume_no_ack=False, wait_time=1):

        while not self._connection.is_closed or self._connection.reconnecting:

            with catch_error():

                message = await self._queue.get(no_ack=consume_no_ack, fail=False)

                if message is None:
                    await Utils.sleep(wait_time)
                else:
                    await consume_func(message)

        Utils.log.warning(f'rabbitmq consumer block pull exit: {consume_func.__name__}')


class RabbitMQConsumerForExchange(RabbitMQConsumer):
    """RabbitMQ注册到交换机的消费者
    """

    def __init__(self, connection: aio_pika.abc.AbstractRobustConnection, queue_name: str, exchange_name: str):
        
        super().__init__(connection, queue_name)

        self._exchange: typing.Optional[aio_pika.abc.AbstractExchange] = None
        self._exchange_name: str = exchange_name

    @property
    def exchange(self) -> aio_pika.abc.AbstractExchange:
        return self._exchange

    @property
    def exchange_name(self) -> str:
        return self._exchange_name

    async def open(
            self, *,
            consume_func=None, consume_no_ack=False, channel_qos_config=None, queue_config=None, routing_key=None
    ):

        await super().open(
            consume_func=consume_func, consume_no_ack=consume_no_ack,
            channel_qos_config=channel_qos_config, queue_config=queue_config
        )

        self._exchange = await self._channel.get_exchange(self._exchange_name)

        await self._queue.bind(self._exchange, routing_key)
