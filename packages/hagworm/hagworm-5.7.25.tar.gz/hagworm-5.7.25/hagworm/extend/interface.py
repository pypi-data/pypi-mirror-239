# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import traceback

from abc import ABC, abstractmethod

from .base import Utils
from .error import Ignore


class FunctorInterface(ABC):
    """仿函数接口定义
    """

    @abstractmethod
    def __call__(self, *args, **kwargs):
        raise NotImplementedError()


class RunnableInterface(ABC):
    """Runnable接口定义
    """

    @abstractmethod
    def run(self, *args, **kwargs):
        raise NotImplementedError()


class TaskInterface(ABC):
    """Task接口定义
    """

    @abstractmethod
    def start(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def stop(self, *args, **kwargs):
        raise NotImplementedError()

    @abstractmethod
    def is_running(self, *args, **kwargs):
        raise NotImplementedError()


class ContextManager(ABC):
    """上下文资源管理器

    子类通过实现_context_release接口，方便的实现with语句管理上下文资源释放

    """

    def __enter__(self):

        self._context_initialize()

        return self

    def __exit__(self, exc_type, exc_value, _traceback):

        self._context_release()

        if exc_type and issubclass(exc_type, Ignore):

            return not exc_value.throw()

        elif exc_value:

            Utils.log.error(traceback.format_exc())

            return True

    def _context_initialize(self):

        pass

    @abstractmethod
    def _context_release(self):

        raise NotImplementedError()


class AsyncContextManager(ABC):
    """异步上下文资源管理器

    子类通过实现_context_release接口，方便的实现with语句管理上下文资源释放

    """

    async def __aenter__(self):

        await self._context_initialize()

        return self

    async def __aexit__(self, exc_type, exc_value, _traceback):

        await self._context_release()

        if exc_type and issubclass(exc_type, Ignore):

            return not exc_value.throw()

        elif exc_value:

            Utils.log.error(traceback.format_exc())

            return True

    async def _context_initialize(self):

        pass

    @abstractmethod
    async def _context_release(self):

        raise NotImplementedError()
