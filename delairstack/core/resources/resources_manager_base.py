"""Resources management.

"""
from .resource import Resource
from ...apis.provider import Provider


class ResourcesManagerBase(object):
    """Base class implementing resources management.

    It provides default implementations of the following operations:

    - Resource creation

    - Search of resources

    - Retrieval of a resource by its identifier

    - Update of a resource

    - Deletion of a resource

    """
    _name = ''

    def __init__(self, *, provider: Provider, **kwargs):
        self._provider = provider

    def create(self, **kwargs) -> Resource:
        """Creates a resource.

        Args:
            **kwargs: Optional keyword arguments used as the
                      description of the resource to create.

        Returns:
            Resource: The created resource.

        """
        content = self._provider.post(path=self._name, data=kwargs)

        return Resource(id=content['_id'], desc=content, manager=self)

    def search(self, *, query) -> [Resource]:
        """Search for resources matching the given query.

        Args:
            query: Query that resources must match.

        Returns:
            [Resource]: List of resources matching the search criteria.

        The argument ``query`` is expected to be JSON serializable.

        """
        content = self._provider.search(path=self._name, query=query)

        return [Resource(id=d['_id'], desc=d, manager=self) for d in content]

    def get(self, *, id: str) -> Resource:
        """Get the resource with given identifier.

        Args:
            id (str): The resource identifire.

        Returns:
            Resource: The resource with identifier equal to ``id``.

        """
        path = '{name}/{id}'.format(name=self._name, id=id)
        content = self._provider.get(path=path)
        return Resource(id=content['_id'], desc=content, manager=self)

    def update(self, *, resource: Resource) -> Resource:
        """Update the resource.

        Args:
            resource (Resource): The resource to update.

        Returns:
            Resource: The updated resource.

        """
        content = self._provider.put(
                path='{name}/{resource_id}'.format(name=self._name, resource_id=resource.id),
                data=resource._desc)
        return Resource(id=content['_id'], desc=content, manager=self)

    def delete(self, *, resource: Resource):
        """Delete the given resource.

        Args:
            resource (Resource): The resource to delete.

        Returns:
            bool: It always returns True.

        """
        self._provider.delete(
                path='{name}/{resource_id}'.format(name=self._name, resource_id=resource.id)
                )
        # if no exceptions is raised
        return True

    def _update_partial(self, id: str, property_name: str, content: dict):
        updated_content = self._provider.put(
                path='{name}/{resource_id}/{property_name}'.format(name=self._name,
                                                                   resource_id=id,
                                                                   property_name=property_name),
                data=content)

        return Resource(id=updated_content['_id'], desc=updated_content, manager=self)
