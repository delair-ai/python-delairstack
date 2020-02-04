"""Implementation of projects.

"""
import copy

from ....core.errors import (QueryError, UnsupportedOperationError,
                             ResponseError)
from ....core.resources.projectmngt.projects import Projects, Project
from ....core.utils.typing import ResourceId, Optional
from ...provider import ProjectManagerAPI, UIServicesAPI


class ProjectsImpl(Projects):
    _hidden = ['dxobjects']
    _immutable = ['created', 'modification_date', 'modification_user',
                  'real_bbox', 'user', 'company', 'missions']

    def __init__(self, project_manager_api: ProjectManagerAPI,
                 ui_services_api: UIServicesAPI, **kwargs):
        super().__init__(provider=project_manager_api,
                         ui_services_api=ui_services_api, **kwargs)
        self._alt_provider = ui_services_api

    def create(self, **kwargs) -> Project:
        """Create a project.

        Args:
            name: Project name.

            geometry: Optional project geometry.

            **kwargs: Optional keyword arguments. Those arguments are
                passed as is to the API provider.

        Raises:
            QueryError: The project creation response is incorrect.

        Returns:
            Project: A resource encapsulating the created project.

        """
        data = copy.copy(kwargs)
        if 'addProjectToUsers' not in data:
            data['addProjectToUsers'] = True
        if 'analytics' not in data:
            data['analytics'] = {}
        if 'linkOrCreateCardinalSite' not in data:
            data['linkOrCreateCardinalSite'] = False

        content = self._alt_provider.post(path=self._name, data=data)
        if 'project' not in content:
            raise QueryError('"project" should be in the response content')
        project_desc = content['project']
        return Project(id=project_desc['_id'], desc=project_desc,
                       manager=self)

    def search(self, *, name: str, deleted: bool = False,
               **kwargs) -> [Project]:
        """Search for projects.

        Args:
            name: Name of the project
                *(the comparison is case insensitive)*.
                ``*`` wildcard is supported

            deleted: Optional parameter to search for deleted project or not
                (``False`` by default).

            **kwargs: Optional keyword arguments. Those arguments are
                passed as is to the API provider.

        Raises:
            QueryError : When the response is not consistent.

        Returns:
            [Project]: List of project resources matching the search criteria.

        Examples:
            Get the projects with a specific name (name is not unique):

            >>> sdk.projects.search(name='My_project')
            [<delairstack.core.resources.projectmngt.projects.Project...>, ...]

            Get all the projects available:

            >>> sdk.projects.search(name='*')
            [<delairstack.core.resources.projectmngt.projects.Project...>, ...]

        """
        data = kwargs
        data.update({'search': name, 'deleted': deleted})
        content = self._alt_provider.post(path='projects/search', data=data)

        if 'projects' not in content:
            raise QueryError(
                '"projects" item should be in the response content')

        return [Project(id=d['_id'], desc=d, manager=self)
                for d in content['projects']]

    def describe(self, project: ResourceId,
                 deleted: bool = False) -> Optional[Project]:
        """Describe the project for the specified id.

        Args:
            project: Project identifier.

            deleted: Optional parameter to describe a deleted project or not
                (``False`` by default).

        Returns:
            Project: Project resource matching the id (``None`` if not found).

        Examples:
            >>> sdk.projects.describe('5ce7f379327e9d5f15e37bb4')
            <delairstack.core.resources.projectmngt.projects.Project ...>

        """
        describe_path = '{}/{}'.format(self._name, project)
        try:
            content = self._alt_provider.post(path=describe_path,
                                              data={'deleted': deleted})
        except ResponseError:
            # When a project is not found, a 404 response is returned
            content = None

        if project not in str(content):
            project_resource = None
        else:
            d = content.get('project')
            project_resource = Project(id=d['_id'], desc=d, manager=self)
        return project_resource

    def update_status(self, project: ResourceId, status: str) -> Project:
        """Update the project status.

        Args:
            project: Project identifier.

            status: Project status (``pending``, ``available``, ``failed``).

        Raises:
            ResponseError : When the project has not been found.

            RuntimeError: The passed status is not allowed.

        Returns:
            Project: Updated project resource.

        """
        available_status = ['pending', 'available', 'failed']
        if status not in available_status:
            raise RuntimeError('Status not in {}'.format(available_status))

        describe_path = '{}/update/{}'.format(self._name, project)
        data = {'project': project, 'status': status}
        content = self._alt_provider.post(path=describe_path, data=data)

        if project not in str(content):
            raise ResponseError(
                'Project {!r} has not been found'.format(project))
        else:
            d = content.get('project')
            project_resource = Project(id=d['_id'], desc=d, manager=self)
        return project_resource

    def delete(self, project: ResourceId) -> None:
        """Delete the specified Project.

        Args:
            project: Identifier of the project to delete.

        """
        self._alt_provider.delete(path='{}/{}'.format('projects', project))
