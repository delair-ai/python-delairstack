from ....apis.provider import ProjectManagerAPI
from ....core.resources.projectmngt.flights import Flights
from ....core.resources.resource import Resource
from delairstack.core.utils.typing import ResourceId


class FlightsImpl(Flights):
    _hidden = ['drone']

    def __init__(self, project_manager_api: ProjectManagerAPI, **kwargs):
        super().__init__(provider=project_manager_api, **kwargs)

    def create(self, *args, **kwargs):
        raise NotImplementedError('missions.create() must be used instead')

    def search(self, *, project: ResourceId = None,
               mission: ResourceId = None) -> [Resource]:
        """Search flights attached to the project mission.

        Args:
            project: The project identifier where flights are searched.

            mission: The mission identifier where flights are searched.

        Returns:
             [Resource]: List of flights found.

        """
        query = {}
        if project is not None:
            query.update({'project_id': project})
        elif mission is not None:
            query.update({'mission_id': mission})

        content = self._provider.search(path=self._name, query=query)

        return [Resource(id=d['_id'], desc=d, manager=self)
                for d in content.get('flights')]
