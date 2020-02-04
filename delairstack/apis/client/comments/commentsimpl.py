"""Implementation of comments.

"""

import os
import urllib.parse

from delairstack.apis.provider import UIServicesAPI

from delairstack.core.errors import ParameterError

from delairstack.core.resources.comments import Comments, Comment
from delairstack.core.resources.resource import Resource

from delairstack.core.utils.typing import List, ResourceId


class CommentsImpl(Comments):
    def __init__(self, ui_services_api: UIServicesAPI,
                 sdk, **kwargs):
        super().__init__(provider=ui_services_api)
        self._sdk = sdk

    def create(self, text: str, *, project: ResourceId,
               type: str, target: ResourceId = None, flight: ResourceId = None,
               **kwargs) -> Comment:
        """Create a comment.

        Args:
            text: Comment content.

            project: Identifier of project to comment.

            type: Comment type (must be one of ``project``, ``annotation``,
                ``flight``, ``photo``, ``dataset``, ``feature``, ``gcp``,
                ``task``).

            target: Optional identifier of the target.

            flight: Optional identifier of the flight (mandatory when the
                comment type is ``photo``).

            **kwargs: Optional keyword arguments. Those arguments are
                passed as is to the API provider.

        Returns:
            Resource: The created comment.

        Examples:
            >>> sdk.comments.create(
            ...    text='my comment',
            ...    project='5d63cf972fb3880011e57f22',
            ...    type='dataset',
            ...    target='5d63cf972fb3880011e57e34')
            <delairstack.core.resources.comments.Comment ... (comments)>

        """
        data = kwargs
        data.update({'project_id': project,
                     'text': text,
                     'target': {'type': type}})

        if type == 'photo':
            if target is None or flight is None:
                raise ParameterError('When commentging a photo, '
                                     'the target and flight must be defined')
            else:
                data['target']['id'] = flight
                data['target']['subId'] = target

        elif target is not None:
            data['target']['id'] = target

        res = self._provider.post('comments', data=data)
        return self._convert_uisrv_desc_to_Comment(desc=res['comment'])

    def _convert_uisrv_desc_to_Comment(self, desc: dict) -> Comment:
        """Convert a comment description returned by UI-Services
           to a Comment object"""
        # {'Comment_key': 'uisrv_desc_key'}
        params = {}

        conversion_dict = {
            'id': '_id',
            'text': 'text',
            'project': 'project_id',
            'creation_date': 'date',
            }

        for k, v in conversion_dict.items():
            if desc.get(v) is not None:
                params[k] = desc.pop(v)

        params['type'] = desc['target'].pop('type')
        if desc['target'].get('subId'):
            params['target'] = desc['target'].pop('subId')
            params['flight'] = desc['target'].pop('id')
        elif desc['target'].get('id'):
            params['target'] = desc['target'].pop('id')
        desc.pop('target')

        params['creation_user'] = desc['author'].pop('id')
        desc.pop('author')

        params.update(desc)  # Save remaining properties (should be empty)

        return Comment(**params)

    def search(self, *, project: ResourceId, type: str = None,
               target: ResourceId = None, flight: ResourceId = None,
               **kwargs) -> List[Resource]:
        """Search for comments.

        When searching for comments on a photo. Both the ``flight`` id and
        ``target`` id must be supplied.

        Args:
            project: Identifier of the project.

            type: Optional comment type (must be one of ``project``,
                ``annotation``, ``flight``, ``photo``, ``dataset``,
                ``feature``, ``gcp``, ``task``).

            target: Optional identifier of the target.

            flight: Optional identifier of the flight (mandatory when the
                comment type is ``photo``).

            **kwargs: Optional keyword arguments. Those arguments are
                passed as is to the API provider.

        Returns:
            Resources: The found comments.

        Examples:
            >>> sdk.comments.search(project='5d63cf972fb3880011e57f22')
            [<delairstack.core.resources.comments.Comment ... (comments)>]

        """
        query = kwargs
        query['project_id'] = project

        if type:
            query['target_type'] = type

        if flight:
            query['target_id'] = flight
            if target:
                # the target is a photo id when a flight id is supplied
                query['target_subid'] = target

        elif target:
            query['target_id'] = target

        query_str = urllib.parse.urlencode(query)
        path = 'comments?{}'.format(query_str)

        desc = self._provider.get(path)

        found_comments = []
        for group in desc.get('conversations'):
            for comment in group.get('comments'):
                comment.update({'target': group.get('_id').copy()})
                comment.update({'project_id': project})
                found_comments.append(
                    self._convert_uisrv_desc_to_Comment(desc=comment))
        return found_comments

    def mark_as_read(self, *, project: ResourceId, type: str = None,
                     target: ResourceId = None, flight: ResourceId = None,
                     **kwargs) -> None:
        """Mark all the comments of a target or project as read.

        Args:
            project: Identifier of project.

            type: Optional comment type (must be one of ``project``,
                ``annotation``, ``flight``, ``photo``, ``dataset``,
                ``feature``, ``gcp``, ``task``).

            target: Optional identifier of the target.

            flight: Optional identifier of the flight (mandatory when the
                comment type is ``photo``).

            **kwargs: Optional keyword arguments. Those arguments are
                passed as is to the API provider.

        Examples:
            >>> sdk.comments.mark_as_read(
            ...    project='5d63cf972fb3880011e57f22',
            ...    type='dataset',
            ...    target='5d63cf972fb3880011e57e34')

        """
        data = kwargs
        data.update({'project_id': project})

        if type:
            data['target'] = {'type': type}
            if type == 'photo':
                if target is None or flight is None:
                    raise ParameterError(
                        'When dealing with a photo target, '
                        'the target and flight must be defined')
                else:
                    data['target']['id'] = flight
                    data['target']['subId'] = target

            elif target is not None:
                data['target']['id'] = target

        self._provider.post('comments/mark-as-read', data=data, as_json=False)
