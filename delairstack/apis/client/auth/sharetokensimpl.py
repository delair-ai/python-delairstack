from delairstack.apis.provider import AuthAPI
from delairstack.core.utils.typing import (List, NamedTuple, Union)
from delairstack.core.utils.typing import ResourceId

from delairstack.core.resources.auth import ShareTokens


ShareToken = dict
ShareTokensWithTotal = NamedTuple('ShareTokensWithTotal',
                                  [('total', int),
                                   ('results', List[ShareToken])])


class ShareTokensImpl(ShareTokens):
    def __init__(self, auth_api: AuthAPI, **kwargs):
        super().__init__(provider=auth_api)

    def create(self, dataset: ResourceId, *,
               company: ResourceId = None,
               duration: int = None,
               **kwargs) -> ShareToken:
        """Create a share token for a given dataset.

        Share token creation is restricted to users with admin profile
        or a manager role on their company.

        Args:
            dataset: Dataset to create a share token for.

            company: Optional identifier of a company to attach the
               created token too. When equal to ``None`` (the
               default), the user company is used.

            duration: Optional duration in seconds of the created
                token. When equal to ``None`` (the default) the
                created token won't expire.

            **kwargs: Optional keyword arguments. Those arguments are
                passed as is to the API provider.

        Returns:
            Dictionary with ``token``, ``expiration_date`` and
            ``scope`` keys.

        Example:
            >>> desc = sdk.share_tokens.create('5d08ebe86a17271b23bc0fcd')
            >>> desc['token'][:16]
            'YfkX6oB5JB02L9x5'

        """
        data = kwargs
        data.update({'scope': {'datasets': {dataset: ['6666']}}})

        if company is not None:
            data['company'] = company

        if duration is not None:
            data['duration'] = duration

        desc = self._provider.post(path='/create-share-token', data=data)
        return desc

    def revoke(self, token: str, company: ResourceId = None, **kwargs):
        """Revoke a share token.

        Share token revocation is restricted to users with admin
        profile or a manager role on their company.

        Args:
            token: Token to revoke.

            company: Optional identifier of a company to search the
               token to revoke. When equal to ``None`` (the default),
               the user company is used.

        Returns:
            **kwargs: Optional keyword arguments. Those arguments are
                passed as is to the API provider.

        """
        data = kwargs
        data.update({'token': token})

        if company is not None:
            data['company'] = company

        self._provider.post(path='/revoke-share-token', data=data,
                            as_json=False)

    def search(self, *, company: ResourceId = None,
               return_total: bool = False,
               **kwargs) -> Union[ShareTokensWithTotal, List[ShareToken]]:
        """Search share tokens.

        Share token search is restricted to users with admin profile
        or a manager role on their company.

        Args:
            company: Optional identifier of a company to filter
               searched tokens. When equal to ``None`` (the default),
               the user company is used.

            return_total: Return the number of results found

        Returns:
            Array of dictionnaries with ``token``, ``expiration_date``
            and ``scope`` keys.

        """
        data = kwargs

        if company is not None:
            data['company'] = company

        desc = self._provider.post(path='/search-share-tokens', data=data)
        tokens = desc.get('results')
        results = [d for d in tokens]

        if return_total is True:
            total = desc.get('total')
            return ShareTokensWithTotal(total=total, results=results)
        else:
            return results
