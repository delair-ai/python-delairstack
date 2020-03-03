import logging
import os

from delairstack.apis.client.annotations.annotationsimpl import AnnotationsImpl
from delairstack.apis.client.comments.commentsimpl import CommentsImpl
from delairstack.apis.client.datamngt.datasetsimpl import DatasetsImpl
from delairstack.apis.client.projectmngt.flightsimpl import FlightsImpl
from delairstack.apis.client.projectmngt.missionsimpl import MissionsImpl
from delairstack.apis.client.projectmngt.projectsimpl import ProjectsImpl
from delairstack.apis.client.auth.sharetokensimpl import ShareTokensImpl
from delairstack.apis.client.tags.tagsimpl import TagsImpl
from delairstack.apis.provider import (AnnotationsAPI, AuthAPI,
                                       DataManagementAPI, ProjectManagerAPI,
                                       UIServicesAPI)
from delairstack.core.config import ConnectionConfig
from delairstack.core.connection.connection import Connection
from delairstack.core.connection.credentials import (ClientCredentials,
                                                     Credentials,
                                                     UserCredentials)
from delairstack.core.errors import ConfigError

__all__ = ('DelairStackSDK', )

LOGGER = logging.getLogger(__name__)


def _get_credentials(config: ConnectionConfig) -> Credentials:
    if getattr(config, 'user', None):
        LOGGER.debug('Using user credentials')
        return UserCredentials(config.user, config.password,
                               client_id=getattr(config, 'client_id', None),
                               secret=getattr(config, 'secret', None),
                               domain=getattr(config, 'domain', None))
    elif getattr(config, 'client_id', None):
        LOGGER.debug('Using APIs client credentials')
        return ClientCredentials(config.client_id,
                                 config.secret)
    return None


def _create_connection(config: ConnectionConfig,
                       credentials: Credentials) -> Connection:
    LOGGER.info('Initializing connection')
    access_token = getattr(config, 'access_token', None)
    if not hasattr(config, 'url'):
        LOGGER.error('Base url not found')
        raise ConfigError('Missing url')

    conn_opts = {'base_url': config.url,
                 'credentials': credentials,
                 'access_token': access_token}

    if hasattr(config, 'proxy_url'):
        LOGGER.info('Use proxy {!r}'.format(config.proxy_url))
        conn_opts.update({'proxy_url': config.proxy_url})

    if hasattr(config, 'connection'):
        for key in ('disable_ssl_certificate', 'max_retries'):
            if key in config.connection:
                conn_opts.update({key: config.connection[key]})

    if credentials is None and access_token is None:
        LOGGER.error('Credentials and access token not found')
        raise ConfigError('Credentials or access token expected')

    try:
        return Connection(**conn_opts)
    except Exception as e:
        LOGGER.error('Cannot establish a connection: {}'.format(e))
        raise e


class DelairStackSDK():
    """Entry point providing access to resource managers.

    Resource managers are availables as instance attributes.
    The ``dir`` builtin can be used to list the availables managers.

    The following examples show various ways to instantiate that
    class:

    - Using a username and a password::

        >>> sdk = DelairStackSDK(user='admin1', password='password')


    - Using an API client identifier and secret::


        >>> sdk = DelairStackSDK(client_id='72a5f676-6efc-48c5-ac07-4c534c3cdccc',
                                 secret='52ccd77d-17e4-499b-995e-3a2731550723')

    - Using a configuration file::

        >>> sdk = DelairStackSDK(config_path='/etc/python-delairstack/conf.json')

    """
    def __init__(self,  *, config_path: str = None,
                 user: str = None, password: str = None,
                 client_id: str = None, secret: str = None,
                 url: str = None, domain: str = None,
                 proxy_url: str = None, **kwargs):
        """Initializes Delair.ai Python SDK entry point.

        Args:
            config_path: Optional path to a custom configuration file.

            user: Optional username (email).

            password: Optional password (mandatory if ``username`` is defined).

            client_id: Optional client identifier.

            secret: Optional client secret (mandatory if ``client_id``
                is defined).

            url: Optional platform URL (default ``https://www.delair.ai``).

            domain: Optional platform domain.

            proxy_url: Optional proxy URL.

            kwargs: Optional keyword arguments to merge with
                           the configuration.

        """
        LOGGER.info('Initializing SDK')

        connection_params = kwargs

        # Only keep defined parameters
        for param_name, value in (('file_path', config_path), ('user', user),
                                  ('password', password),
                                  ('client_id', client_id),
                                  ('secret', secret), ('url', url),
                                  ('domain', domain),
                                  ('proxy_url', proxy_url)):
            if value is not None:
                connection_params[param_name] = value

        for env_var in ('https_proxy', 'HTTPS_PROXY',
                        'http_proxy', 'HTTP_PROXY'):
            env_var_value = os.environ.get(env_var)
            if env_var_value is not None:
                connection_params['proxy_url'] = env_var_value
                LOGGER.info(
                    'Found environment variable {!r} with value: {!r}'.format(
                        env_var, env_var_value)
                )
                break

        connection_config = ConnectionConfig(**connection_params)
        credentials = _get_credentials(connection_config)
        self._connection = _create_connection(connection_config, credentials)

        token = self._connection._token_manager.token
        if not token.access_token or not token.token_type:
            self._connection._renew_token()

        self.__set_providers()
        self.__set_resources_as_attributes()

    def __set_providers(self):
        provider_args = {'connection': self._connection}
        self._providers = {
            'annotations_api': AnnotationsAPI(**provider_args),
            'auth_api': AuthAPI(**provider_args),
            'data_management_api': DataManagementAPI(**provider_args),
            'project_manager_api': ProjectManagerAPI(**provider_args),
            'ui_services_api': UIServicesAPI(**provider_args)
        }

    def __set_resources_as_attributes(self):
        kwargs = {'sdk': self}
        kwargs.update(self._providers)

        self.annotations = AnnotationsImpl(**kwargs)
        self.comments = CommentsImpl(**kwargs)
        self.datasets = DatasetsImpl(**kwargs)
        self.flights = FlightsImpl(**kwargs)
        self.missions = MissionsImpl(**kwargs)
        self.projects = ProjectsImpl(**kwargs)
        self.share_tokens = ShareTokensImpl(**kwargs)
        self.tags = TagsImpl(**kwargs)
