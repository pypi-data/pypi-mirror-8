from __future__ import absolute_import

from datetime import timedelta
from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from django.db import models
from functools import partial
from krankshaft import valid
from krankshaft.api import API as APIBase
from krankshaft.auth import Auth as AuthBase
from krankshaft.authn import Authn
from krankshaft.authz import Authz
from krankshaft.exceptions import KrankshaftError
from krankshaft.resource import DjangoModelResource
from krankshaft.throttle import Throttle
from tempfile import NamedTemporaryFile
from tests.base import TestCaseNoDB
import json
import pytest
import sys

class Auth(AuthBase):
    authn = Authn()
    authz = Authz(require_authned=False)

class API(APIBase):
    Auth = Auth


class AuthzDeny(Authz):
    def is_authorized_request(self, request, authned):
        return False

class AuthDeny(AuthBase):
    authn = Authn()
    authz = AuthzDeny()

class APIDeny(APIBase):
    Auth = AuthDeny

ThrottleOne = partial(
    Throttle,
    anon_bucket=timedelta(seconds=2),
    anon_rate=(1, timedelta(seconds=10)),
    bucket=timedelta(seconds=2),
    cache=cache,
    rate=(1, timedelta(seconds=10))
)

class FakeAPIMany(models.Model):
    char_indexed = models.CharField(max_length=20, db_index=True)

class FakeAPI(models.Model):
    char_indexed = models.CharField(max_length=20, db_index=True)
    manytomany = models.ManyToManyField(FakeAPIMany)

class FakeAPI2(models.Model):
    char_indexed = models.CharField(max_length=20, db_index=True)

class Fake1(models.Model):
    name = models.CharField(max_length=20)

class Fake2(models.Model):
    fake1 = models.ForeignKey(Fake1)

class APITest(TestCaseNoDB):
    def _pre_setup(self):
        self.api = API('v1')
        self.apid = API('v1', debug=True)
        self.api_error = API('v1', debug=True, error='custom error message')
        self.api1 = API('v1')
        self.api2 = API('v1')
        self.api2.include(self.api1)

        @self.api1
        class Fake1Resource(DjangoModelResource):
            model = Fake1

        @self.api2
        class Fake2Resource(DjangoModelResource):
            model = Fake2

        @self.api1
        def plainview(request):
            return self.api1.response(request, 200)

        super(APITest, self)._pre_setup()

        # make sure cache is clear
        cache.clear()

    def test_abort(self):
        request = self.make_request()
        self.assertRaises(self.api.Abort, self.api.abort, request, 401)
        try:
            self.api.abort(request, 401)
        except Exception, exc:
            self.assertEquals(401, exc.response.status_code)

        response = self.api.response(request, 401)
        try:
            self.api.abort(response)
        except Exception, exc:
            self.assertEquals(response, exc.response)

        self.assertRaises(
            KrankshaftError,
            self.api.abort,
            response,
            Header=''
        )
        self.assertRaises(
            TypeError,
            self.api.abort,
            request
        )

    def test_annotate(self):
        def fakeview(request):
            return \
                hasattr(request, 'auth') \
                and isinstance(request.auth, self.api.Auth) \
                and not hasattr(request, 'user')
        fakeview = self.api(fakeview)

        request = self.make_request()
        request.user = AnonymousUser()
        self.assertEqual(hasattr(request, 'auth'), False)
        self.assertEqual(fakeview(request), True)
        self.assertEqual(hasattr(request, 'auth'), False)

    def test_auth_deny(self):
        response = self.client.get('/deny/?key=value')
        self.assertEquals(response.status_code, 401)
        self.assertTrue(not response.content)

    def test_auth_deny_decorator_only(self):
        response = self.client.get('/deny-decorator-only/?key=value')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response['Content-Type'].split(';')[0],
            'application/json'
        )
        self.assertEquals(
            json.loads(response.content),
            {'key': 'value'}
        )

    def test_auth_deny_manual(self):
        response = self.client.get('/deny-decorator-only-manual/')
        self.assertEquals(response.status_code, 401)
        self.assertTrue(not response.content)

    def test_deserialize_delete_get_head_options(self):
        for method in (
            self.client.delete,
            self.client.get,
            self.client.head,
            self.client.options,
        ):
            response = method('/serialize-payload/?key=value&key2=value2')
            self.assertEquals(response.status_code, 200)
            self.assertEquals(
                response['Content-Type'].split(';')[0],
                'application/json'
            )
            if method not in (self.client.head,):
                self.assertEquals(
                    json.loads(response.content),
                    {'key': 'value', 'key2': 'value2'}
                )

    def test_deserialize_post_put_form_types(self):
        for method in (
            self.client.post,
            self.client.put,
        ):
            response = method(
                '/serialize-payload/',
                'key=value&key2=value2',
                content_type='application/x-www-form-urlencoded'
            )
            self.assertEquals(response.status_code, 200)
            self.assertEquals(
                response['Content-Type'].split(';')[0],
                'application/json'
            )
            self.assertEquals(
                json.loads(response.content),
                {'key': 'value', 'key2': 'value2'}
            )

            response = method(
                '/serialize-payload/',
                {'key': 'value', 'key2': 'value2'}
            )
            self.assertEquals(response.status_code, 200)
            self.assertEquals(
                response['Content-Type'].split(';')[0],
                'application/json'
            )
            self.assertEquals(
                json.loads(response.content),
                {'key': 'value', 'key2': 'value2'}
            )

            tmp = NamedTemporaryFile()
            tmp.write('value\n')
            tmp.seek(0)
            response = method('/serialize-payload/', {'file': tmp})
            self.assertEquals(response.status_code, 200)
            self.assertEquals(
                response['Content-Type'].split(';')[0],
                'application/json'
            )
            self.assertEquals(
                json.loads(response.content),
                {'file': 'value\n'}
            )
            tmp.close()

    def test_deserialize_invalid_content(self):
        response = self.client.post(
            '/serialize-payload/',
            '!',
            content_type='application/json'
        )
        self.assertEquals(response.status_code, 400)

    def test_deserialize_invalid_content_length(self):
        request = self.make_request('POST',
            data='{"key": "value"}',
            content_type='application/json',
            CONTENT_LENGTH='a'
        )
        query, data = self.api.deserialize(request)
        self.assertTrue(not data)

    def test_deserialize_invalid_content_nonabortable(self):
        request = self.make_request('POST',
            data='!',
            content_type='application/json'
        )
        self.assertRaises(
            ValueError,
            self.api.deserialize,
            request,
            abortable=False
        )

    def test_deserialize_unsupported_content_type(self):
        response = self.client.post(
            '/serialize-payload/',
            '!',
            content_type='unsupported/content-type'
        )
        self.assertEquals(response.status_code, 406)

    def test_deserialize_unsupported_content_type_nonabortable(self):
        request = self.make_request('POST',
            data='!',
            content_type='unsupported/content-type'
        )
        self.assertRaises(
            self.api.serializer.Unsupported,
            self.api.deserialize,
            request,
            abortable=False
        )

    def test_deserialize_invalid_query_string(self):
        response = self.client.get('/serialize-payload/?key=value&invalid')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response['Content-Type'].split(';')[0],
            'application/json'
        )
        self.assertEquals(
            json.loads(response.content),
            {'key': 'value', 'invalid': ''}
        )

    def test_defaults_dispatch_empty(self):
        self.assertEqual(self.api.options_dispatch({}), self.api.defaults_dispatch)

    def test_defaults_dispatch_none(self):
        self.assertEqual(self.api.options_dispatch(None), self.api.defaults_dispatch)

    def test_defaults_dispatch_badopt(self):
        self.assertRaises(
            self.api.InvalidOptions,
            self.api.options_dispatch,
            {'__badopt': True}
        )

    def test_expect(self):
        self.assertEqual(
            self.api.expect({'key': valid.int}, {'key': '1'}),
            {'key': 1}
        )

    def test_expect_fail(self):
        self.assertRaises(
            self.api.ValueIssue,
            self.api.expect,
            {'key': valid.int},
            {'key': 'a'}
        )

    def test_handle_exc_abort(self):
        request = self.make_request()
        try:
            self.api.abort(request, 400)
        except Exception:
            response = self.api.handle_exc(request)

        self.assertEquals(response.status_code, 400)

    def test_handle_exc_unhandled_exception(self):
        request = self.make_request()
        try:
            {}['key']
        except Exception:
            response = self.api.handle_exc(request)

        self.assertEquals(response.status_code, 500)
        self.assertEquals(
            response['Content-Type'].split(';')[0],
            'application/json'
        )

        data = json.loads(response.content)
        self.assertEquals(data['error'], self.api.error)
        self.assertTrue('exception' not in data)
        self.assertTrue('traceback' not in data)

    def test_handle_exc_unhandled_exception_debug(self):
        request = self.make_request()
        try:
            {}['key']
        except Exception:
            response = self.apid.handle_exc(request)

        self.assertEquals(response.status_code, 500)
        self.assertEquals(
            response['Content-Type'].split(';')[0],
            'application/json'
        )

        data = json.loads(response.content)
        self.assertEquals(data['error'], self.apid.error)
        self.assertEquals(data['exception'], "KeyError: 'key'")
        self.assertTrue(data['traceback'])

    def test_handle_exc_unhandled_exception_debug_custom(self):
        request = self.make_request()
        try:
            {}['key']
        except Exception:
            response = self.apid.handle_exc(request, error='myerror')

        self.assertEquals(response.status_code, 500)
        self.assertEquals(
            response['Content-Type'].split(';')[0],
            'application/json'
        )

        data = json.loads(response.content)
        self.assertEquals(data['error'], 'myerror')
        self.assertEquals(data['exception'], "KeyError: 'key'")
        self.assertTrue(data['traceback'])

    def test_handle_exc_unhandled_exception_debug_custom_init(self):
        request = self.make_request()
        try:
            {}['key']
        except Exception:
            response = self.api_error.handle_exc(request)

        self.assertEquals(response.status_code, 500)
        self.assertEquals(
            response['Content-Type'].split(';')[0],
            'application/json'
        )

        data = json.loads(response.content)
        self.assertEquals(data['error'], self.api_error.error)
        self.assertEquals(data['exception'], "KeyError: 'key'")
        self.assertTrue(data['traceback'])

    def test_handle_exc_unhandled_exception_debug_specific(self):
        request = self.make_request()
        try:
            {}['key']
        except Exception:
            exc_info_keyerror = sys.exc_info()

        try:
            [][1]
        except Exception:
            exc_info_indexerror = sys.exc_info()
            response = self.apid.handle_exc(request, exc_info=exc_info_keyerror)

        self.assertEquals(response.status_code, 500)
        self.assertEquals(
            response['Content-Type'].split(';')[0],
            'application/json'
        )

        data = json.loads(response.content)
        self.assertEquals(data['error'], self.apid.error)
        self.assertEquals(data['exception'], "KeyError: 'key'")
        self.assertTrue(data['traceback'])

    def test_include(self):
        fake1 = Fake1.objects.create(id=1, name='fake1')
        fake2 = Fake2.objects.create(id=1, fake1=fake1)

        response = self.client.get(self.api2.reverse('fake2_single', args=(1,)))
        assert response.status_code == 200
        assert json.loads(response.content) == {
            'id': 1,
            'fake1': '/app1/api/v1/fake1/1/',
            'fake1_id': 1,
            '_id': 1,
            '_pk': 'id',
            '_uri': '/app2/api/v1/fake2/1/',
        }

    def test_include_api1_again(self):
        self.assertRaises(self.api2.Error, self.api2.include, self.api1)

    def test_include_deep(self):
        api = API('v1')
        api2 = API('v1')
        api3 = API('v1')

        api.include(api2, deep=True)
        api2.include(api3)

        @api3
        def apiv3view(request):
            pass

        assert apiv3view in api.registered_views

    def test_include_self(self):
        self.assertRaises(self.api2.Error, self.api2.include, self.api2)

    def test_method_get(self):
        response = self.client.get('/only-post/')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'POST')

    def test_method_post(self):
        response = self.client.post('/only-post/')
        self.assertEqual(response.status_code, 200)

    def test_redirect(self):
        request = self.make_request()
        for code in (301, 302):
            response = self.api.redirect(request, code, '/hello world/')
            self.assertEquals(response.status_code, code)
            self.assertEquals(response['Location'], '/hello%20world/')

    def test_redirect_abort(self):
        request = self.make_request()
        for code in (301, 302):
            try:
                self.api.abort(self.api.redirect(request, code, '/'))
            except Exception, e:
                self.assertEquals(e.response.status_code, code)
                self.assertEquals(e.response['Location'], '/')

    def test_register(self):
        self.assertRaises(self.api.Error, self.api.register, None, url=())
        self.assertRaises(self.api.Error, self.api.register, None, url=(1,2,3,4,5))
        self.assertRaises(self.api.Error, self.api.register, None, url=object())

    def test_response(self):
        response = self.api.response(
            self.make_request(),
            200,
            'content',
            Content_Type='text/plain'
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.content, 'content')
        self.assertEquals(
            response['Content-Type'].split(';')[0],
            'text/plain'
        )

    def test_schema(self):
        response = self.client.get('/app1/api/v1/')
        assert response.status_code == 200
        assert json.loads(response.content) == {
            'resources': {
                'fake1': {
                    'doc': None,
                    'endpoint': {
                        'list': {
                            'allow': ['PUT', 'POST', 'DELETE', 'GET'],
                            'docs': {
                                'DELETE': '\n        Deletes the instances pointed to by the given query (specified by\n        the query string).\n\n            /resource/?field=value\n\n        ',
                                'GET': '\n        Get the serialized value of a list of objects of a given query\n        (specified as the query string).\n\n            /resource/?field=value\n\n        ',
                                'POST': '\n        Create a new object.\n\n            /resource/\n\n        ',
                                'PUT': '\n        Given a single dictionary of fields and values, update all the instances\n        with the given field/values.\n\n        Ideally, a subset of all fields is given.  Enables mass update to\n        an unknown set of objects (those matching a query).\n\n            /resource/?field=value\n\n        '
                            },
                            'params': [],
                            'url': '/app1/api/v1/fake1/'
                        },
                        'set': {
                            'allow': ['PUT', 'DELETE', 'GET'],
                            'docs': {
                                'DELETE': '\n        Delete the given set of objects (specified in the path as an id list\n        separated by a semi-colon).\n\n            /resource/set/1;2;3/\n\n        ',
                                'GET': '\n        Get the serialized value of a set of objects given by a list of ids\n        separated by a semi-colon.\n\n            /resource/set/1;2;3/\n\n        ',
                                'PUT': '\n        Update a set of objects.\n\n            /resource/set/1;2;3/\n\n        '
                            },
                            'params': ['idset'],
                            'url': '/app1/api/v1/fake1/set/:idset/'
                        },
                        'single': {
                            'allow': ['PUT', 'DELETE', 'GET'],
                            'docs': {
                                'DELETE': '\n        Deletes the object pointed to by id.\n\n            /resource/1/\n\n        ',
                                'GET': '\n        Get the serialized value of an object.\n\n            /resource/1/\n\n        ',
                                'PUT': '\n        Update an object.\n\n            /resource/1/\n\n        '
                            },
                            'params': ['id'],
                            'url': '/app1/api/v1/fake1/:id/'
                        },
                    },
                    'fields': {
                        'id': {
                            'help_text': '',
                            'indexed': True,
                            'max_length': None,
                            'nullable': False,
                            'type': 'AutoField'
                        },
                        'name': {
                            'help_text': '',
                            'indexed': False,
                            'max_length': 20,
                            'nullable': False,
                            'type': 'CharField'
                        }
                    },
                    'url': '/app1/api/v1/fake1/'
                },
                'plainview': {
                    'url': '',
                    'doc': None,
                    'endpoint': {}
                },
            }
        }

    def test_serialize(self):
        data = {'one': 1}
        request = self.make_request(HTTP_ACCEPT='application/json; indent=4')
        response = self.api.serialize(request, 200, data)
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response['Content-Type'].split(';')[0],
            'application/json'
        )
        self.assertEquals(response.content, json.dumps(data, indent=4))

    def test_serialize_default_browser_accept(self):
        data = {'one': 1}
        request = self.make_request(HTTP_ACCEPT='*/*')
        response = self.api.serialize(request, 200, data)
        assert response.status_code == 200
        assert response['Content-Type'] == 'application/json; charset=utf-8'
        assert json.loads(response.content) == {'one': 1}

    def test_serialize_force_content_type(self):
        data = {'one': 1}
        request = self.make_request(HTTP_ACCEPT='application/xml')
        response = self.api.serialize(request, 200, data,
            content_type='application/json'
        )
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response['Content-Type'].split(';')[0],
            'application/json'
        )
        self.assertEquals(response.content, json.dumps(data))

    def test_throttle(self):
        response = self.client.get('/throttle/?key=value')
        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response['Content-Type'].split(';')[0],
            'application/json'
        )
        self.assertEquals(
            json.loads(response.content),
            {'key': 'value'}
        )

        response = self.client.get('/throttle/?key=value')
        self.assertEquals(response.status_code, 429)
        self.assertTrue(not response.content)
        self.assertEquals(response['Retry-After'], '13')

    @property
    def urls(self):
        from django.conf.urls import include, url
        return self.make_urlconf(
            url('^deny/$',
                self.api(self.view_serialize_payload, auth=AuthDeny)
            ),
            url('^deny-decorator-only/$',
                self.api(auth=AuthDeny, only=True)(self.view_serialize_payload)
            ),
            url('^deny-decorator-only-manual/$',
                self.api(only=True)(self.view_auth_manual)
            ),
            url('^only-post/$', self.api(self.view_serialize_payload, methods=('POST', ))),
            url('^serialize-payload/$', self.api(self.view_serialize_payload)),
            url('^throttle/$',
                self.api(self.view_serialize_payload, throttle=ThrottleOne)
            ),
            url('^app1/api/', include(self.api1.urls)),
            url('^app2/api/', include(self.api2.urls)),
        )

    def view_auth_manual(self, request):
        auth = self.api.auth(request, Auth=AuthDeny)
        if auth:
            return self.api.serialize(request, 200, {'authed': True})

        else:
            return auth.challenge(self.api.response(request, 401))

    def view_serialize_payload(self, request):
        query, data = self.api.deserialize(request)

        for key, value in data.items():
            if hasattr(value, 'read'):
                data[key] = value.read()

        query.update(data)

        return self.api.serialize(request, 200, query)


@pytest.mark.django_db
class APIResourceTest(TestCaseNoDB):
    def _pre_setup(self):
        self.api = API('v1')
        super(APIResourceTest, self)._pre_setup()

    def test_django_model_resource_resolve(self):
        FakeAPI.objects.create(id=1, char_indexed='value1')
        FakeAPI.objects.create(id=2, char_indexed='value2')
        FakeAPI.objects.create(id=3, char_indexed='value3')
        resource, ids = self.api.resolve([
            '/api/v1/fakeapi/2/',
            '/api/v1/fakeapi/3/',
            '/api/v1/fakeapi/1/',
        ])
        assert ids == ['2', '3', '1']

        instances = resource.fetch(*ids)
        assert [
            instance.pk
            for instance in instances
        ] == [2, 3, 1]

    def test_django_model_resource_resolve_many_resources(self):
        self.assertRaises(self.api.ResolveError, self.api.resolve, [
            '/api/v1/fakeapi/1/',
            '/api/v1/fakeapi2/1/',
        ])

    def test_django_model_resource_resolve_doesnotexist(self):
        resource, ids = self.api.resolve(['/api/v1/fakeapi/999/'])
        self.assertRaises(FakeAPI.DoesNotExist, resource.fetch, *ids)

    def test_django_model_resource_resolve_nothing(self):
        self.assertRaises(self.api.ResolveError, self.api.resolve, [])

    def test_django_model_resource_resolve_not_found(self):
        self.assertRaises(self.api.ResolveError, self.api.resolve, '/not/a/valid/path/')

    def test_django_model_resource_resolve_non_resource(self):
        self.assertRaises(self.api.ResolveError, self.api.resolve, '/resource/nomethods/')

    def test_django_model_resource_reverse(self):
        assert self.api.reverse('fakeapi_list') == '/api/v1/fakeapi/'
        assert self.api.reverse('fakeapi_single', args=(1,)) == '/api/v1/fakeapi/1/'
        assert self.api.reverse('fakeapi_set', args=('1;2;3', )) == '/api/v1/fakeapi/set/1;2;3/'

    def test_ensure_failure_to_assign_url_with_resource_with_urls(self):
        api = API('v1')

        class Resource(object):
            def router(self):
                pass

            @property
            def urls(self):
                from django.conf.urls import patterns
                return patterns('',
                    (r'^resource/other/$', api.wrap(self.router)),
                )

        self.assertRaises(api.Error, api, Resource, url=r'^resource/$')

    def test_resource_no_methods(self):
        for method in [
            getattr(self.client, name)
            for name in self.api.methods
        ]:
            response = method('/resource/nomethods/')
            self.assertEqual(response.status_code, 405)
            self.assertEqual(response['Allow'], '')

    def test_resource_get_only(self):
        response = self.client.post('/resource/get-only/')
        self.assertEqual(response.status_code, 405)
        self.assertEqual(response['Allow'], 'GET')

    def test_resource_simple_get(self):
        response = self.client.get('/resource/simple/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '1')

    def test_resource_simple_post(self):
        response = self.client.post('/resource/simple/1/')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content, '10')

    def test_response_with_name(self):
        from django.core.urlresolvers import reverse
        response = self.client.get(reverse(self.api.endpoint('view_name')))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'view_name')

    def test_response_with_name_with_api_reverse(self):
        response = self.client.get(self.api.reverse('view_name'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'view_name')

    def test_response_with_router(self):
        response = self.client.get('/resource/with-router/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'response')

    def test_response_with_urls(self):
        response = self.client.get('/api/v1/resource/with-urls/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'with-urls')

    def test_response_with_urls_with_router_reuse_single(self):
        response = self.client.get('/api/v1/resource/with-urls-with-router-reuse/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"single": 1}')

    def test_response_with_urls_with_router_reuse_set(self):
        response = self.client.get('/api/v1/resource/with-urls-with-router-reuse/set/1;2;3;4;5;6/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, '{"set": [1, 2, 3, 4, 5, 6]}')

    def test_view_with_url(self):
        response = self.client.get('/api/v1/view/with-url/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'view-with-url')

    def test_view_with_url_id(self):
        response = self.client.get('/api/v1/view/with-url/1/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, 'view-with-url-1-option')

    @property
    def urls(self):
        from django.conf.urls import include, url

        api = self.api

        class ResourceNoMethods(object):
            pass

        class ResourceGetOnly(object):
            def get(self):
                pass

        class ResourceSimple(object):
            def get(self, request, id):
                return api.response(request, 200, str(id))

            def post(self, request, id):
                return api.response(request, 201, str(int(id) * 10))

        class ResourceWithRouter(object):
            def route(self, request, args, kwargs):
                return self.response(request, *args, **kwargs)

            def response(self, request, *args, **kwargs):
                return api.response(request, 200, 'response')

        @api
        class ResourceWithURLs(object):
            def router(self, request, *args, **kwargs):
                return self.api.response(request, 200, 'with-urls')

            @property
            def urls(self):
                from django.conf.urls import patterns
                return patterns('',
                    (r'^resource/with-urls/$', self.api.wrap(self.router)),
                )

        @api
        class ResourceWithURLsWithRouterReuse(object):
            def get(self, request, id):
                return self.api.serialize(request, 200, {
                    'single': int(id)
                })

            def get_set(self, request, idset):
                return self.api.serialize(request, 200, {
                    'set': [int(id) for id in idset.split(';')]
                })

            def route_set(self, request, *args, **kwargs):
                return self.api.route({
                    'get': self.get_set,
                }, request, args, kwargs)

            def route_single(self, request, *args, **kwargs):
                return self.api.route({
                    'get': self.get,
                }, request, args, kwargs)

            @property
            def urls(self):
                from django.conf.urls import patterns
                return patterns('',
                    (r'^resource/with-urls-with-router-reuse/(?P<id>\d+)/$', self.api.wrap(self.route_single)),
                    (r'^resource/with-urls-with-router-reuse/set/(?P<idset>\d[\d;]*)/$', self.api.wrap(self.route_set)),
                )

        @api(url='^view/with-url/$')
        def view_with_url(request):
            return api.response(request, 200, 'view-with-url')

        @api(url=('^view/with-url/(?P<id>\d+)/$', {'extra': 'option'}))
        def view_with_url(request, id, extra=None):
            return api.response(request, 200, 'view-with-url-%s-%s' % (id, extra))

        @api(url='^view/name/$')
        def view_name(request):
            return api.response(request, 200, 'view_name')

        @api
        class FakeAPIResource(DjangoModelResource):
            model = FakeAPI

        @api
        class FakeAPI2Resource(DjangoModelResource):
            model = FakeAPI2

        return self.make_urlconf(
            url('^resource/nomethods/$', api(ResourceNoMethods)),
            url('^resource/get-only/$', api(ResourceGetOnly)),
            url('^resource/simple/(?P<id>\d+)/$', api(ResourceSimple)),
            url('^resource/with-router/$', api(ResourceWithRouter)),
            url('^api/', include(api.urls)),
        )
