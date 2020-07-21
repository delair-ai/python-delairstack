"""
    Credential implementation
"""

from delairstack.apis.provider import ExternalProviderServiceAPI
from delairstack.core.resources.credentials import Credentials
from delairstack.core.utils.typing import (Dict, List, Resource, ResourceId,
                                           ResourcesWithTotal, Union)


class CredentialsImpl(Credentials):
    def __init__(self,
                 external_provider_service_api: ExternalProviderServiceAPI,
                 **kwargs):
        super().__init__(provider=external_provider_service_api, **kwargs)

    def search(self, *, name: str = None, filter: Dict = None,
               limit: int = None, page: int = None, sort: dict = None,
               return_total: bool = False,
               **kwargs) -> Union[ResourcesWithTotal, List[Resource]]:
        """Search for a list of credentials.

        Args:
            name: Credential name.

            filter: Search filter dictionary (refer to ``/search-credentials``
                definition in the External Providers Service API for a detailed
                description of ``filter``).

            limit: Maximum number of results to extract.

            page: Page number (starting at page 0).

            sort: Sort the results on the specified attributes
                (``1`` is sorting in ascending order,
                ``-1`` is sorting in descending order).

            return_total: Return the number of results found.

            **kwargs: Optional keyword arguments. Those arguments are
                passed as is to the API provider.

        Returns:
            Credentials: A list of credential resources OR a namedtuple
                with total number of results and list of credential resources.

        """
        data = kwargs

        for prop_name, value in [('filter', filter or {}),
                                 ('limit', limit),
                                 ('page', page),
                                 ('sort', sort)]:
            if value is not None:
                data.update({prop_name: value})

        if name is not None:
            data['filter']['name'] = {'$eq': name}

        search_desc = self._provider.post(
            path='search-credentials', data=data, as_json=True)

        credentials = search_desc.get('results')

        results = [Resource(id=credentials['_id'], desc=credentials,
                   manager=self) for credentials in credentials]

        if return_total is True:
            total = search_desc.get('total')
            return ResourcesWithTotal(total=total, results=results)
        else:
            return results

    def create(self, *, name: str, credentials: Dict[str, str],
               **kwargs) -> Resource:
        """Create a credential entry.

        Args:
            name: Credential name (must be unique).

            credentials: Credential dict.

            **kwargs: Optional keyword arguments. Those arguments are
                passed as is to the API provider.

        Returns:
            The created credential description.

        Examples:
            >>> sdk.credentials.create(name="My Docker registry",
            ...     credentials={
            ...         "type": "docker",
            ...         "login": "my_login",
            ...         "password": "my_password",
            ...         "registry": "mydockerregistry.com"
            ...     }
            ... )
            <delairstack.core.resources.Resource with id ... (credentials)>

            >>> sdk.credentials.create(name="My Docker registry",
            ...     credentials={
            ...         "type": "aws",
            ...         "aws_access_key_id": "key_id",
            ...         "aws_secret_access_key": "password_test",
            ...         "aws_region": "us-east-1",
            ...         "registry": "XXX..dkr.ecr.us-east-1.amazonaws.com"
            ...     }
            ... )
            <delairstack.core.resources.Resource with id ... (credentials)>

        """
        data = kwargs

        data.update({
            'name': name,
            'credentials': credentials
        })

        desc = self._provider.post(
            path='create-credentials', data=dict(data), as_json=True)

        return Resource(id=desc['_id'], desc=desc, manager=self)

    def delete(self, credential: ResourceId, **kwargs) -> None:
        """Delete a credential entry.

        Args:
            credential: Credential identifier.

            **kwargs: Optional keyword arguments. Those arguments are
                passed as is to the API provider.

        """
        data = kwargs
        data.update({'credentials':  credential})

        self._provider.post(
            path='delete-credentials',
            data=data,
            as_json=False
        )
