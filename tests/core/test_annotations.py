import json

from urllib3_mock import Responses

from delairstack.core.errors import (QueryError, ParameterError)
from delairstack.core.resources.resource import Resource
from .resource_test_base import ResourcesTestBase

responses = Responses('requests.packages.urllib3')


class TestAnnotations(ResourcesTestBase):
    """Test annotations.

    """
    @responses.activate
    def test_search(self):
        responses.add('POST', '/map-service/annotations/search-annotations',
                      body=json.dumps({'results': [{'_id': 'annotation-id'}]}),
                      status=200,
                      content_type='application/json')

        self.sdk.annotations.search(project='project-id')

        calls = responses.calls
        self.assertEqual(len(calls), 1)

        self.assertEqual(calls[0].request.url,
                         '/map-service/annotations/search-annotations')
        self.assertEqual(calls[0].request.method, 'POST')

        request_body = json.loads(calls[0].request.body)
        self.assertEqual(request_body['filter'],
                         {'project': {'$eq': 'project-id'}})


class TestAnnotationsLegacy(ResourcesTestBase):
    """Test legacy SDK interface for annotations.

    """
    @responses.activate
    def test_create_from_feature(self):
        responses.add('POST', '/map-service/annotations/create-annotation',
                      body=self.__annotation(), status=200,
                      content_type='application/json')

        xmin = 4.387072438909058
        xmax = 8.034533376409058
        ymin = 44.48207258784539
        ymax = 47.26550167777244

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Polygon',
                'coordinates': [[[xmin, ymax], [xmax, ymax], [xmax, ymin],
                                 [xmin, ymin], [xmin, ymax]]]
                }
            }

        with self.assertWarns(DeprecationWarning):
            self.sdk.annotations.create(project='project-id',
                                        feature=feature)

        calls = responses.calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].request.url,
                         '/map-service/annotations/create-annotation')
        self.assertEqual(calls[0].request.method, 'POST')

        request_body = json.loads(calls[0].request.body)
        self.assertTrue('project' in request_body)
        self.assertTrue('type' in request_body)
        self.assertTrue('geometry' in request_body)

        self.assertEqual(request_body['project'], 'project-id')
        self.assertEqual(request_body['type'], '2d')
        self.assertEqual(request_body['geometry'], feature['geometry'])

    @responses.activate
    def test_create_from_feature_with_properties(self):
        responses.add('POST', '/map-service/annotations/create-annotation',
                      body=self.__annotation(), status=200,
                      content_type='application/json')

        project_id = 'project-id'

        xmin = 4.387072438909058
        xmax = 8.034533376409058
        ymin = 44.48207258784539
        ymax = 47.26550167777244

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Polygon',
                'coordinates': [[[xmin, ymax], [xmax, ymax], [xmax, ymin],
                                 [xmin, ymin], [xmin, ymax]]]
                },
            'properties': {
                'name': 'My Polygon',
                'comment': 'Test a polygon annotation'
                }
            }

        with self.assertWarns(DeprecationWarning):
            self.sdk.annotations.create(project=project_id, feature=feature)

        calls = responses.calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].request.url,
                         '/map-service/annotations/create-annotation')
        self.assertEqual(calls[0].request.method, 'POST')

        request_body = json.loads(calls[0].request.body)
        self.assertTrue('project' in request_body)
        self.assertTrue('type' in request_body)
        self.assertTrue('geometry' in request_body)

        self.assertEqual(request_body['project'], 'project-id')
        self.assertEqual(request_body['type'], '2d')
        self.assertEqual(request_body['geometry'], feature['geometry'])
        self.assertEqual(request_body['name'], feature['properties']['name'])
        self.assertEqual(request_body['description'],
                         feature['properties']['comment'])

    @responses.activate
    def test_create_from_feature_with_image(self):
        responses.add('POST', '/map-service/annotations/create-annotation',
                      body=self.__annotation(), status=200,
                      content_type='application/json')

        xmin = 4.387072438909058
        xmax = 8.034533376409058
        ymin = 44.48207258784539
        ymax = 47.26550167777244

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Polygon',
                'coordinates': [[[xmin, ymax], [xmax, ymax], [xmax, ymin],
                                 [xmin, ymin], [xmin, ymax]]]
                },
            'properties': {
                'name': 'My Polygon',
                'comment': 'Test a polygon annotation'
                }
            }

        with self.assertWarns(DeprecationWarning):
            self.sdk.annotations.create(project='project-id',
                                        feature=feature,
                                        flight='flight-id',
                                        image='image-id')

        calls = responses.calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].request.url,
                         '/map-service/annotations/create-annotation')
        self.assertEqual(calls[0].request.method, 'POST')

        request_body = json.loads(calls[0].request.body)
        self.assertTrue('project' in request_body)
        self.assertTrue('type' in request_body)
        self.assertTrue('geometry' in request_body)
        self.assertTrue('target' in request_body)

        self.assertEqual(request_body['project'], 'project-id')
        self.assertEqual(request_body['target'],
                         {'type': 'dataset', 'id': 'image-id'})
        self.assertEqual(request_body['type'], '2d')
        self.assertEqual(request_body['geometry'], feature['geometry'])
        self.assertEqual(request_body['name'], feature['properties']['name'])
        self.assertEqual(request_body['description'],
                         feature['properties']['comment'])

    @responses.activate
    def test_create_from_feature_with_target(self):
        responses.add('POST', '/map-service/annotations/create-annotation',
                      body=self.__annotation(), status=200,
                      content_type='application/json')

        xmin = 4.387072438909058
        xmax = 8.034533376409058
        ymin = 44.48207258784539
        ymax = 47.26550167777244

        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Polygon',
                'coordinates': [[[xmin, ymax], [xmax, ymax], [xmax, ymin],
                                 [xmin, ymin], [xmin, ymax]]]
                },
            'properties': {
                'name': 'My Polygon',
                'comment': 'Test a polygon annotation'
                }
            }

        with self.assertWarns(DeprecationWarning):
            self.sdk.annotations.create(project='project-id',
                                        feature=feature,
                                        dataset='mesh-id',
                                        target='3d')

        calls = responses.calls
        self.assertEqual(len(calls), 1)
        self.assertEqual(calls[0].request.url,
                         '/map-service/annotations/create-annotation')
        self.assertEqual(calls[0].request.method, 'POST')

        request_body = json.loads(calls[0].request.body)
        self.assertTrue('project' in request_body)
        self.assertTrue('type' in request_body)
        self.assertTrue('geometry' in request_body)
        self.assertTrue('target' in request_body)

        self.assertEqual(request_body['project'], 'project-id')
        self.assertEqual(request_body['target'],
                         {'type': 'dataset', 'id': 'mesh-id'})
        self.assertEqual(request_body['type'], '3d')
        self.assertEqual(request_body['geometry'], feature['geometry'])
        self.assertEqual(request_body['name'], feature['properties']['name'])
        self.assertEqual(request_body['description'],
                         feature['properties']['comment'])

    @responses.activate
    def test_update_without_changes(self):
        responses.add('PUT', '/map-service/annotations/rename-annotation',
                      body=self.__annotation(), status=200,
                      content_type='application/json')

        annotation = Resource(id='annotation-id',
                              desc={'name': 'unit annotation'})

        with self.assertRaises(QueryError):
            with self.assertWarns(DeprecationWarning):
                annotation = self.sdk.annotations.update(resource=annotation)

    @responses.activate
    def test_update_feature_properties(self):
        responses.add('POST', '/map-service/annotations/rename-annotation',
                      body=self.__annotation(), status=200,
                      content_type='application/json')
        responses.add('POST',
                      '/map-service/annotations/set-annotation-description',
                      body=self.__annotation(), status=200,
                      content_type='application/json')
        responses.add('POST',
                      '/map-service/annotations/describe-annotation',
                      body=self.__annotation(), status=200,
                      content_type='application/json')

        annotation = Resource(id='annotation-id',
                              desc={'name': 'unit annotation'})

        feature = {
            'properties': {
                'name': 'My Polygon',
                'comment': 'Test a polygon annotation'
                }
            }

        annotation.feature = feature
        with self.assertWarns(DeprecationWarning):
            self.sdk.annotations.update(resource=annotation)

        calls = responses.calls
        self.assertEqual(len(calls), 3)
        self.assertEqual(calls[0].request.url,
                         '/map-service/annotations/rename-annotation')
        self.assertEqual(calls[0].request.method, 'POST')
        request_body = json.loads(calls[0].request.body)
        self.assertEqual(request_body['name'], feature['properties']['name'])

        self.assertEqual(calls[1].request.url,
                         '/map-service/annotations/set-annotation-description')
        self.assertEqual(calls[1].request.method, 'POST')
        request_body = json.loads(calls[1].request.body)
        self.assertEqual(request_body['description'],
                         feature['properties']['comment'])

        self.assertEqual(calls[2].request.url,
                         '/map-service/annotations/describe-annotation')
        self.assertEqual(calls[2].request.method, 'POST')

    @responses.activate
    def test_update_feature_geometry(self):
        responses.add('POST', '/map-service/annotations/set-annotation-geometry',
                      body=self.__annotation(), status=200,
                      content_type='application/json')
        responses.add('POST',
                      '/map-service/annotations/describe-annotation',
                      body=self.__annotation(), status=200,
                      content_type='application/json')

        annotation = Resource(id='annotation-id',
                              desc={'name': 'unit annotation'})

        feature = {'geometry': 'geom'}
        annotation.feature = feature
        with self.assertWarns(DeprecationWarning):
            self.sdk.annotations.update(resource=annotation)

        calls = responses.calls
        self.assertEqual(len(calls), 2)
        self.assertEqual(calls[0].request.url,
                         '/map-service/annotations/set-annotation-geometry')
        self.assertEqual(calls[0].request.method, 'POST')
        request_body = json.loads(calls[0].request.body)
        self.assertEqual(request_body['geometry'], feature['geometry'])

        self.assertEqual(calls[1].request.url,
                         '/map-service/annotations/describe-annotation')
        self.assertEqual(calls[1].request.method, 'POST')

    @responses.activate
    def test_update_feature_properties_unmanaged(self):
        annotation = Resource(id='annotation-id',
                              desc={'name': 'unit annotation'})

        feature = {'properties': 'prop'}
        annotation.feature = feature
        with self.assertRaises(QueryError):
            with self.assertWarns(DeprecationWarning):
                self.sdk.annotations.update(resource=annotation)

    def __annotation(self):
        return json.dumps({
            "_id": "annotation-id"
            })
