"""Analytics implementation
"""

from collections import defaultdict

from delairstack.core.resources.resource import Resource
from delairstack.apis.provider import AnalyticsServiceAPI
from delairstack.core.resources.analytics.analytics import Analytics
from delairstack.core.resources.analytics.products import Products
from delairstack.core.utils.typing import (Dict, List, ResourceId,
                                           ResourcesWithTotal, Union)


class AnalyticsImpl(Analytics):
    def __init__(self, analytics_service_api: AnalyticsServiceAPI, **kwargs):
        super().__init__(provider=analytics_service_api, **kwargs)

    def search(self, *, name: str = None, filter: Dict = None,
               limit: int = None, page: int = None, sort: dict = None,
               return_total: bool = False,
               **kwargs) -> Union[ResourcesWithTotal, List[Resource]]:
        """Search for a list of analytics.

        Args:
            name: Analytic name.

            filter: Search filter dictionary (refer to ``/search-analytics``
                definition in the Analytics-service API for a detailed description
                of ``filter``).

            limit: Maximum number of results to extract.

            page: Page number (starting at page 0).

            sort: Sort the results on the specified attributes
                (``1`` is sorting in ascending order,
                ``-1`` is sorting in descending order).

            return_total: Return the number of results found.

            **kwargs: Optional keyword arguments. Those arguments are
                passed as is to the API provider.

        Returns:
            Analytics: A list of analytics resources OR a namedtuple
                with total number of results and list of analytics resources.

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
            path='search-analytics', data=data, as_json=True)

        analytics = search_desc.get('results')

        results = [Resource(id=analytic['_id'], desc=analytic, manager=self)
                   for analytic in analytics]

        if return_total is True:
            total = search_desc.get('total')
            return ResourcesWithTotal(total=total, results=results)
        else:
            return results

    def describe(self, analytic: ResourceId, **kwargs) -> Resource:
        """Describe an analytic.

        Args:
            analytic: Identifier of the analytic to describe.

            **kwargs: Optional keyword arguments. Those arguments are
                passed as is to the API provider.

        Returns:
            The analytic description.

        """
        data = kwargs

        data['analytic'] = analytic
        desc = self._provider.post('describe-analytic', data=data)
        return Resource(id=desc['_id'], desc=desc, manager=self)

    def create(self, *, name: str, docker_image: str,
               display_name: str = None, description: str = None,
               instance_type: str = None, volume_size: int = None,
               inputs: List[dict] = None, parameters: List[dict] = None,
               deliverables: List[dict] = None, outputs: List[dict] = None,
               tags: List[str] = None, groups: List[str] = None,
               **kwargs) -> Resource:
        """Create an analytic.

        Args:
            name: Analytic name (must be unique).

            docker_image: Docker image used for the analytic computation,
                including the Docker registry address.
                (example: ``"gcr.io/myproject/myanalytic:v1.0"``).

            display_name: Optional user-friendly name of the analytic.

            description: Optional analytic description.

            instance_type: Optional instance type on which the analytic
                will be run (example: ``"small"``).

            volume_size: Optional size of the attached volume (in gigabytes).

            inputs: Optional inputs of the analytic.

            parameters: Optional parameters of the analytic.

            deliverables: Optional deliverables of the analytic.

            outputs: Optional outputs of the analytic.

            tags: Optional tags of the analytic.

            groups: Optional groups of the analytic (used by the analytic
                catalogue on the front-end to group analytics).

            **kwargs: Optional keyword arguments. Those arguments are
                passed as is to the API provider.

        Returns:
            The created analytic description.

        Raise:
            KeyError: When a passed value is not supported.

        Examples:
            >>> sdk.analytics.create(name="my_vehicle_detection",
            ...     display_name="Vehicle detection",
            ...     description="Detects vehicles in orthomosaic images",
            ...     docker_image="gcr.io/myproject/vehicule-detection:v1.0",
            ...     instance_type='large',
            ...     volume_size=50,
            ...     inputs=[{
            ...         "name": "ortho",
            ...         "display_name": "Orthomosaic",
            ...         "description": "Orthomosaic",
            ...         "scheme": {
            ...             "type": "string", "pattern": "^[0-9a-f]{24}$"
            ...         },
            ...         "source": {
            ...             "service": "data-manager", "resource": "dataset",
            ...             "scheme": {
            ...                 "type": "object",
            ...                 "properties": {"type": {"const": "raster"}},
            ...                 "required": ["type"]
            ...             },
            ...         },
            ...         "required": True
            ...     }],
            ...     parameters=[{
            ...         "name": "project",
            ...         "display_name": "Project",
            ...         "description": "Project identifier",
            ...         "required": True,
            ...         "scheme": {
            ...             "type": "string", "pattern": "^[0-9a-f]{24}$"
            ...         }
            ...      }],
            ...     deliverables=[{
            ...         "name": "positions",
            ...         "display_name": "Vehicule positions",
            ...         "description": "Position of the vehicules in a CSV",
            ...         "scheme": {
            ...             "type": "string", "pattern": "^[0-9a-f]{24}$"
            ...         },
            ...         "source": {
            ...             "service": "data-manager", "resource": "dataset",
            ...             "scheme": {
            ...                 "type": "object",
            ...                 "properties": {"type": {"const": "file"}},
            ...                 "required": ["type"]
            ...             },
            ...         },
            ...         "required": True
            ...     }],
            ...      tags=["vehicle_detection"],
            ...      groups=["GeoInt"])
            <delairstack.core.resources.Resource with id ... (analytic)>

        """
        data = defaultdict(dict)
        data.update(kwargs)

        data['name'] = name
        data['algorithm']['docker_image'] = docker_image

        if instance_type:
            data['instance']['type'] = instance_type
        if volume_size:
            data['instance']['volume'] = volume_size

        for k, v in [
            ('display_name', display_name),
            ('description', description),
            ('inputs', inputs), ('parameters', parameters),
            ('deliverables', deliverables), ('outputs', outputs),
            ('tags', tags), ('groups', groups)
        ]:
            if v:
                data.update({k: v})

        desc = self._provider.post(
            path='create-analytic', data=dict(data), as_json=True)

        return Resource(id=desc['_id'], desc=desc, manager=self)

    def delete(self, analytic: Union[ResourceId, List[ResourceId]], *,
               permanent: bool = False, **kwargs) -> None:
        """Delete an analytic or a list of analytics.

        Args:
            analytic: Analytic identifier (or list of identifiers) to delete.

            permanent: Whether to delete analytics permanently or not.
                Default to False.

            **kwargs: Optional keyword arguments. Those arguments are
                passed as is to the API provider.

        """
        if not isinstance(analytic, list):
            analytic = [analytic]

        data = {'analytics':  analytic}
        data.update(kwargs)

        path = 'delete-analytics' if not permanent \
            else 'delete-analytics-permanently'

        self._provider.post(path=path, data=data, as_json=False)

    def order(self, analytic: ResourceId, *, inputs: dict = None,
              parameters: dict = None, deliverables: List[str] = None,
              project: ResourceId = None, mission: ResourceId = None,
              **kwargs) -> Resource:
        """Order an analytic.

        Args:
            analytic: Identifier of the analytic to order.

            inputs: Optional inputs of the analytic.

            parameters: Optional parameters of the analytic.

            deliverables: List of optional deliverables to generate.
                When empty or ``None`` only required deliverables are generated.

            project: Optional project of the analytic.

            mission: Optional mission of the analytic.

            **kwargs: Optional keyword arguments. Those arguments are
                passed as is to the API provider.

        Returns:
            The created ``product`` description.

        Examples:
            >>> sdk.analytics.order(analytic='5d5a73b58cf5360006397aa0',
            ...     inputs={"ortho": "5d3714e14c50356e2abd1f97"},
            ...     deliverables=["vehicles"],
            ...     parameters={"project": "5d3195209755b0349d0539ad"},
            ...     project='5d3195209755b0349d0539ad')
            <delairstack.core.resources.Resource with id ... (product)>

        """
        data = {'analytic': analytic}

        # Update to the format expected by analytics-service
        if deliverables:
            deliverables = {d: None for d in deliverables}

        for k, v in [('inputs', inputs), ('parameters', parameters),
                     ('deliverables', deliverables),
                     ('project', project), ('mission', mission)]:
            if v:
                data.update({k: v})

        data.update(kwargs)

        desc = self._provider.post(path='order-analytic', data=data)

        return Resource(id=desc['_id'], desc=desc, manager=Products)
