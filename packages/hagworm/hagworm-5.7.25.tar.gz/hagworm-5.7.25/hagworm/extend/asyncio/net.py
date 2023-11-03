# -*- coding: utf-8 -*-

__author__ = r'wsb310@gmail.com'

import typing
import httpx

from contextlib import contextmanager
from httpx import _types

from .base import Utils, AsyncCirculatoryForSecond


DEFAULT_RETRIES = 5
DEFAULT_TIMEOUT = httpx.Timeout(timeout=60)
DEFAULT_LIMITS = httpx.Limits(max_connections=200, max_keepalive_connections=50)
DOWNLOAD_TIMEOUT = httpx.Timeout(timeout=600)


@contextmanager
def _catch_error():
    """异常捕获

    通过with语句捕获异常，代码更清晰，还可以使用Ignore异常安全的跳出with代码块

    """

    try:

        yield

    except httpx.HTTPStatusError as err:

        Utils.log.warning(err)

    except Exception as err:

        Utils.log.error(err)


class Result(dict):

    def __init__(self, status: int, headers: typing.Dict, cookies: typing.Dict, body: typing.Any):

        super().__init__(status=status, headers=headers, cookies=cookies, body=body)

    def __bool__(self):

        return (self.status >= 200) and (self.status <= 299)

    @property
    def status(self) -> int:

        return self.get(r'status')

    @property
    def headers(self) -> typing.Dict:

        return self.get(r'headers')

    @property
    def cookies(self) -> typing.Dict:

        return self.get(r'cookies')

    @property
    def body(self) -> typing.Any:

        return self.get(r'body')


class _ClientBase:

    def __init__(
            self,
            verify: _types.VerifyTypes = False,
            limits: httpx.Limits = DEFAULT_LIMITS,
            timeout: _types.TimeoutTypes = DOWNLOAD_TIMEOUT,
            **kwargs
    ):

        self._client: httpx.AsyncClient = httpx.AsyncClient(verify=verify, limits=limits, timeout=timeout, **kwargs)

    async def close(self):

        if not self._client.is_closed:
            await self._client.aclose()


class HTTPClientPool(_ClientBase):
    """HTTP客户端类
    """

    def __init__(self,
                 retries: int = DEFAULT_RETRIES,
                 verify: _types.VerifyTypes = False,
                 limits: httpx.Limits = DEFAULT_LIMITS,
                 timeout: _types.TimeoutTypes = DEFAULT_TIMEOUT,
                 **kwargs
                 ):

        self._retries: int = retries

        super().__init__(verify=verify, limits=limits, timeout=timeout, **kwargs)

    def _handle_response(self, response: httpx.Response) -> bytes:

        return response.content

    async def send_request(
            self,
            method: str,
            url: _types.URLTypes,
            *,
            content: typing.Optional[_types.RequestContent] = None,
            data: typing.Optional[_types.RequestData] = None,
            files: typing.Optional[_types.RequestFiles] = None,
            json: typing.Optional[typing.Any] = None,
            params: typing.Optional[_types.QueryParamTypes] = None,
            headers: typing.Optional[_types.HeaderTypes] = None,
            cookies: typing.Optional[_types.CookieTypes] = None,
            **kwargs
    ) -> Result:

        response = None

        async for times in AsyncCirculatoryForSecond(max_times=self._retries):

            try:

                _resp = await self._client.request(
                    method, url,
                    content=content, data=data, files=files, json=json, params=params,
                    headers=headers, cookies=cookies,
                    **kwargs
                )

                response = Result(
                    _resp.status_code,
                    dict(_resp.headers),
                    dict(_resp.cookies),
                    self._handle_response(_resp)
                )

            except httpx.HTTPStatusError as err:

                # 重新尝试的话，会记录异常，否则会继续抛出异常

                if err.response.status_code < 500:
                    raise err
                elif times >= self._retries:
                    raise err
                else:
                    Utils.log.warning(err)
                    continue

            except (httpx.TimeoutException, httpx.NetworkError) as err:

                if times >= self._retries:
                    raise err
                else:
                    Utils.log.warning(err)
                    continue

            else:

                Utils.log.info(f'{method} {url} => status:{response.status}')
                break

            finally:

                if times > 1:
                    Utils.log.warning(f'{method} {url} => retry:{times}')

        return response

    async def close(self):

        if not self._client.is_closed:
            await self._client.aclose()

    async def get(
            self,
            url: _types.URLTypes,
            *,
            params: typing.Optional[_types.QueryParamTypes] = None,
            headers: typing.Optional[_types.HeaderTypes] = None,
            cookies: typing.Optional[_types.CookieTypes] = None
    ) -> typing.Any:

        with _catch_error():

            resp = await self.send_request(r'GET', url, params=params, headers=headers, cookies=cookies)

            return resp.body

    async def options(
            self,
            url: _types.URLTypes,
            *,
            params: typing.Optional[_types.QueryParamTypes] = None,
            headers: typing.Optional[_types.HeaderTypes] = None,
            cookies: typing.Optional[_types.CookieTypes] = None
    ) -> typing.Any:

        with _catch_error():

            resp = await self.send_request(r'OPTIONS', url, params=params, headers=headers, cookies=cookies)

            return resp.headers

    async def head(
            self,
            url: _types.URLTypes,
            *,
            params: typing.Optional[_types.QueryParamTypes] = None,
            headers: typing.Optional[_types.HeaderTypes] = None,
            cookies: typing.Optional[_types.CookieTypes] = None
    ) -> typing.Any:

        with _catch_error():

            resp = await self.send_request(r'HEAD', url, params=params, headers=headers, cookies=cookies)

            return resp.headers

    async def post(
            self,
            url: _types.URLTypes,
            *,
            content: typing.Optional[_types.RequestContent] = None,
            data: typing.Optional[_types.RequestData] = None,
            files: typing.Optional[_types.RequestFiles] = None,
            json: typing.Optional[typing.Any] = None,
            params: typing.Optional[_types.QueryParamTypes] = None,
            headers: typing.Optional[_types.HeaderTypes] = None,
            cookies: typing.Optional[_types.CookieTypes] = None
    ) -> typing.Any:

        with _catch_error():

            resp = await self.send_request(
                r'POST', url,
                content=content, data=data, files=files, json=json, params=params,
                headers=headers, cookies=cookies
            )

            return resp.body

    async def put(
            self,
            url: _types.URLTypes,
            *,
            content: typing.Optional[_types.RequestContent] = None,
            data: typing.Optional[_types.RequestData] = None,
            files: typing.Optional[_types.RequestFiles] = None,
            json: typing.Optional[typing.Any] = None,
            params: typing.Optional[_types.QueryParamTypes] = None,
            headers: typing.Optional[_types.HeaderTypes] = None,
            cookies: typing.Optional[_types.CookieTypes] = None
    ) -> typing.Any:

        with _catch_error():

            resp = await self.send_request(
                r'PUT', url,
                content=content, data=data, files=files, json=json, params=params,
                headers=headers, cookies=cookies
            )

            return resp.body

    async def patch(
            self,
            url: _types.URLTypes,
            *,
            content: typing.Optional[_types.RequestContent] = None,
            data: typing.Optional[_types.RequestData] = None,
            files: typing.Optional[_types.RequestFiles] = None,
            json: typing.Optional[typing.Any] = None,
            params: typing.Optional[_types.QueryParamTypes] = None,
            headers: typing.Optional[_types.HeaderTypes] = None,
            cookies: typing.Optional[_types.CookieTypes] = None
    ) -> typing.Any:

        with _catch_error():

            resp = await self.send_request(
                r'PATCH', url,
                content=content, data=data, files=files, json=json, params=params,
                headers=headers, cookies=cookies
            )

            return resp.body

    async def delete(
            self,
            url: _types.URLTypes,
            *,
            content: typing.Optional[_types.RequestContent] = None,
            data: typing.Optional[_types.RequestData] = None,
            files: typing.Optional[_types.RequestFiles] = None,
            json: typing.Optional[typing.Any] = None,
            params: typing.Optional[_types.QueryParamTypes] = None,
            headers: typing.Optional[_types.HeaderTypes] = None,
            cookies: typing.Optional[_types.CookieTypes] = None
    ) -> typing.Any:

        with _catch_error():

            resp = await self.send_request(
                r'DELETE', url,
                content=content, data=data, files=files, json=json, params=params,
                headers=headers, cookies=cookies
            )

            return resp.body


class HTTPTextClientPool(HTTPClientPool):
    """HTTP客户端，Text模式
    """

    def _handle_response(self, response: httpx.Response) -> str:

        return response.text


class HTTPJsonClientPool(HTTPClientPool):
    """HTTP客户端，Json模式
    """

    def _handle_response(self, response: httpx.Response) -> typing.Union[typing.Dict, typing.List]:

        return response.json()


class Downloader(_ClientBase):
    """HTTP文件下载器
    """

    async def fetch(
            self,
            file: typing.BinaryIO,
            url: _types.URLTypes,
            *,
            chunk_size: int = 65536,
            params: typing.Optional[_types.QueryParamTypes] = None,
            headers: typing.Optional[_types.HeaderTypes] = None,
            cookies: typing.Optional[_types.CookieTypes] = None
    ) -> bool:

        result = False

        async with self._client.stream(r'GET', url, params=params, headers=headers, cookies=cookies) as response:

            async for chunk in response.aiter_bytes(chunk_size):
                file.write(chunk)
            else:
                result = True

        return result
