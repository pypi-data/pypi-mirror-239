# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import pytz
import typing
import asyncio
import logging
import functools

from abc import abstractmethod

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from ..trace import refresh_trace_id
from ..interface import TaskInterface

from .base import Utils


TIMEZONE = pytz.timezone(r'Asia/Shanghai')


logging.getLogger(r'apscheduler').setLevel(logging.ERROR)


class TaskAbstract(TaskInterface):
    """任务基类
    """

    def __init__(self, scheduler=None):

        global TIMEZONE

        self._scheduler = AsyncIOScheduler(
            job_defaults={
                r'coalesce': False,
                r'max_instances': 1,
                r'misfire_grace_time': 10
            },
            timezone=TIMEZONE
        ) if scheduler is None else scheduler

    @property
    def scheduler(self):

        return self._scheduler

    @staticmethod
    def _func_wrapper(func, *args, **kwargs):

        @functools.wraps(func)
        async def _wrapper():
            refresh_trace_id()
            return await Utils.awaitable_wrapper(func(*args, **kwargs))

        return _wrapper

    def is_running(self):

        return self._scheduler.running

    def start(self):

        return self._scheduler.start()

    def stop(self):

        return self._scheduler.shutdown()

    @abstractmethod
    def add_job(self):

        raise NotImplementedError()

    def remove_job(self, job_id):

        return self._scheduler.remove_job(job_id)

    def remove_all_jobs(self):

        return self._scheduler.remove_all_jobs()


class IntervalTask(TaskAbstract):
    """间隔任务类
    """

    @classmethod
    def create(cls, interval, func, *args, **kwargs):

        inst = cls()

        inst.add_job(interval, func, *args, **kwargs)

        return inst

    def add_job(self, interval, func, *args, **kwargs):

        return self._scheduler.add_job(
            self._func_wrapper(func, *args, **kwargs),
            r'interval', seconds=interval
        )


class CronTask(TaskAbstract):
    """定时任务类
    """

    @classmethod
    def create(cls, crontab, func, *args, **kwargs):

        inst = cls()

        inst.add_job(crontab, func, *args, **kwargs)

        return inst

    def add_job(self, crontab, func, *args, **kwargs):

        return self._scheduler.add_job(
            self._func_wrapper(func, *args, **kwargs),
            CronTrigger.from_crontab(crontab, TIMEZONE)
        )


class DCSCronTask(TaskInterface):

    def __init__(self, redis_client, name, crontab, func, *args, **kwargs):

        self._name = name

        self._task_lock = redis_client.allocate_lock(f'dcs_cron_task:{name}', timeout=60)
        self._task_func = func

        self._heartbeat = IntervalTask.create(30, self._do_heartbeat)
        self._cron_task = CronTask.create(crontab, self._do_job, *args, **kwargs)

    @property
    def name(self):

        return self._name

    async def _do_heartbeat(self):

        resp = await self._check_status()

        Utils.log.debug(f'dcs cron task heartbeat: {self._name} => {resp}')

    async def _check_status(self):

        if await self._task_lock.acquire():
            return True
        else:
            return False

    async def _do_job(self, *args, **kwargs):

        if await self._check_status():

            Utils.log.info(f'dcs cron task start: {self._name}')

            if Utils.is_coroutine_function(self._task_func):
                await self._task_func(*args, **kwargs)
            else:
                self._task_func(*args, **kwargs)

            Utils.log.info(f'dcs cron task finish: {self._name}')

        else:

            Utils.log.debug(f'dcs cron task idle: {self._name}')

    def start(self, min_delay=30, max_delay=60):

        delay = Utils.randint(min_delay, max_delay)

        def _func():
            self._heartbeat.start()
            self._cron_task.start()
            Utils.log.info(f'dcs cron task init: {self._name}, delay: {delay}')

        if delay == 0:
            _func()
        else:
            Utils.call_later(delay, _func)

    def stop(self):

        self._heartbeat.stop()
        self._cron_task.stop()

    def is_running(self):

        return self._cron_task.is_running()


class MultiTasks:
    """多任务并发管理器

    提供协程的多任务并发的解决方案

    tasks = MultiTasks()
    tasks.append(func1())
    tasks.append(func2())
    ...
    tasks.append(funcN())
    await tasks

    多任务中禁止使用上下文资源共享的对象(如mysql和redis等)
    同时需要注意类似这种不能同时为多个协程提供服务的对象会造成不可预期的问题

    """

    def __init__(self):

        self._coroutines: typing.List[typing.Coroutine] = []

    def __await__(self) -> typing.List[typing.Any]:

        result = None

        if len(self._coroutines) > 0:

            result = yield from asyncio.gather(*self._coroutines).__await__()

            self._coroutines.clear()

        return result

    def __len__(self) -> int:

        return self._coroutines.__len__()

    def append(self, coroutine: typing.Coroutine):

        return self._coroutines.append(coroutine)

    def extend(self, coroutines: typing.List[typing.Coroutine]):

        return self._coroutines.extend(coroutines)

    def clear(self):

        for coroutine in self._coroutines:
            coroutine.close()

        self._coroutines.clear()


class SliceTasks(MultiTasks):
    """多任务分片并发管理器

    继承自MultiTasks类，通过参数tasks_num控制并发分片任务数

    """

    def __init__(self, tasks_num: int):

        super().__init__()

        self._tasks_num = max(1, tasks_num)

    def __await__(self) -> typing.List[typing.Any]:

        result = []

        if len(self._coroutines) > 0:

            for _idx in range(0, len(self._coroutines), self._tasks_num):

                tasks = self._coroutines[_idx: _idx + self._tasks_num]

                result.extend(
                    (yield from asyncio.gather(*tasks).__await__())
                )

            self._coroutines.clear()

        return result


class QueueTasks(MultiTasks):
    """多任务队列管理器

    继承自MultiTasks类，通过参数tasks_num控制队列长度

    """

    def __init__(self, tasks_num: int):

        super().__init__()

        self._tasks_num: int = max(1, tasks_num)

        self._semaphore: asyncio.Semaphore = asyncio.Semaphore(self._tasks_num)

    def __await__(self) -> typing.List[typing.Any]:

        result = None

        if len(self._coroutines) > 0:

            tasks = [self._do_task(_task) for _task in self._coroutines]

            result = yield from asyncio.gather(*tasks).__await__()

            self._coroutines.clear()

        return result

    async def _do_task(self, coroutine: typing.Coroutine):

        async with self._semaphore:
            return await coroutine


class RateLimiter:
    """流量控制器，用于对计算资源的保护
    添加任务append函数如果成功会返回Future对象，可以通过await该对象等待执行结果
    进入队列的任务，如果触发限流行为会通过在Future上引发CancelledError传递出来
    """

    def __init__(self, running_limit: int, waiting_limit: int = 0, timeout: float = 0):

        self._timeout: float = timeout

        self._task_queue: asyncio.Queue[
            typing.Tuple[typing.Callable, typing.Tuple, typing.Dict, float]
        ] = asyncio.Queue(waiting_limit)

        self._consume_tasks: typing.List[asyncio.Task] = [
            asyncio.create_task(self._do_consume_task()) for _ in range(running_limit)
        ]

    def size(self) -> int:

        return self._task_queue.qsize()

    async def close(self):

        await self._task_queue.join()

        for task in self._consume_tasks:
            task.cancel()

        self._consume_tasks.clear()

    async def wait(self):

        return await self._task_queue.join()

    async def append(self, func: typing.Callable, *args, **kwargs) -> bool:

        result = False

        with Utils.suppress(asyncio.TimeoutError):

            await asyncio.wait_for(
                self._task_queue.put(
                    (func, args, kwargs, Utils.loop_time())
                ),
                self._timeout if self._timeout > 0 else None
            )

            result = True

        return result

    async def _do_consume_task(self):

        while True:

            try:

                func, args, kwargs, build_time = await self._task_queue.get()

                if (self._timeout > 0) and ((Utils.loop_time() - build_time) > self._timeout):
                    Utils.log.warning(f'rate limit timeout: {func} build_time:{build_time}')
                    continue

                await Utils.awaitable_wrapper(func(*args, **kwargs))

            except asyncio.CancelledError as err:

                raise err

            except Exception as err:

                Utils.log.error(str(err))

            finally:

                self._task_queue.task_done()
