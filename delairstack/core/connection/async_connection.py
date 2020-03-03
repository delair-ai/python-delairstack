import concurrent.futures as cf
import logging
from threading import Lock
from urllib.parse import urljoin

from requests.adapters import HTTPAdapter
from requests_futures.sessions import FuturesSession

from .abstract_connection import AbstractConnection

LOGGER = logging.getLogger(__name__)


class AsyncConnection(AbstractConnection):
    def __init__(self, *, base_url, disable_ssl_certificate,
                 token_manager, retries, max_requests_workers=6,
                 proxy_url=None):
        super().__init__(base_url=base_url,
                         disable_ssl_certificate=disable_ssl_certificate,
                         token_manager=token_manager, retries=retries)

        executor = cf.ThreadPoolExecutor(max_workers=max_requests_workers)
        adapter_kwargs = {'pool_connections': max_requests_workers,
                          'pool_maxsize': max_requests_workers,
                          'max_retries': self._retries,
                          'pool_block': True}
        self._asession = FuturesSession(executor=executor)
        self._asession.mount('https://', HTTPAdapter(**adapter_kwargs))
        self._asession.mount('http://', HTTPAdapter(**adapter_kwargs))
        if proxy_url is not None:
            self._asession.proxies = {
                'http': proxy_url,
                'https': proxy_url,
            }
        self._access_token_lock = Lock()
        self._max_requests_workers = max_requests_workers

    @property
    def executor(self):
        return self._asession.executor

    @property
    def max_request_workers(self):
        return self._max_requests_workers

    def _add_authorization_maybe(self, headers: dict, url: str):
        with self._access_token_lock:
            super()._add_authorization_maybe(headers, url)

    def post(self, path, headers=None, callback=None, data=None, timeout=30.0):
        url = urljoin(self._base_url, path)
        params = {'method': 'POST',
                  'url': url,
                  'headers': headers,
                  'data': data,
                  'verify': (not self._disable_ssl_certificate),
                  'timeout': timeout}
        return self._send_request(params, on_finish_callback=callback)

    def put(self, path, headers=None, callback=None, files=None, timeout=30.0):
        url = urljoin(self._base_url, self._encode_spaces(path))
        params = {'method': 'PUT',
                  'url': url,
                  'headers': headers,
                  'files': files,
                  'verify': (not self._disable_ssl_certificate),
                  'timeout': timeout}
        return self._send_request(params=params, on_finish_callback=callback)

    def _send_request(self, params, on_finish_callback):
        params['headers'] = params['headers'] or {}
        self._add_authorization_maybe(params['headers'], params['url'])
        self._add_user_agent(params['headers'])
        try:
            token = params['headers']['Authorization'].split('Bearer')[1].strip()
        except KeyError:
            token = None

        def extended_callback(response, *args, **kwargs):
            if response.status_code == 401:
                LOGGER.debug('Got a 401 status')
                skip = self._skip_token_renewal(params['url'])
                if not skip:
                    with self._access_token_lock:  # block concurrent send requests
                        renewed = (token != self._token_manager.token.access_token)
                        if renewed:
                            LOGGER.debug('Token already renewed')
                        else:
                            self._renew_token()

            if on_finish_callback:
                on_finish_callback(response)

        c_params = params
        c_params['hooks'] = {'response': extended_callback}
        LOGGER.debug('Making request {} to {}'.format(params['method'],
                                                      params['url']))
        return self._asession.request(**c_params)
