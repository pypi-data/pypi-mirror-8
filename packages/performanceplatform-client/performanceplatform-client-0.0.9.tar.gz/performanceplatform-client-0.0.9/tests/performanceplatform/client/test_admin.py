
import mock
import multiprocessing

from nose.tools import eq_
from requests import Response
from hamcrest import has_entries, match_equality, starts_with

from performanceplatform.client.admin import AdminAPI


class TestAdminAPI(object):

    @mock.patch('requests.get')
    def test_get_has_correct_headers(self, mock_get):
        mock_get.__name__ = 'get'
        api = AdminAPI('http://admin.api', 'token')
        api.list_data_sets()

        mock_get.assert_called_with(
            'http://admin.api/data-sets',
            headers=match_equality(has_entries({
                'Accept': 'application/json',
                'Authorization': 'Bearer token',
                'User-Agent': starts_with('Performance Platform Client'),
            }))
        )

    @mock.patch('requests.get')
    def test_get_user(self, mock_get):
        mock_get.__name__ = 'get'
        api = AdminAPI('http://admin.api', 'token')
        api.get_user('foo@bar.com')

        mock_get.assert_called_with(
            'http://admin.api/users/foo%40bar.com',
            headers=match_equality(has_entries({
                'Accept': 'application/json',
                'Authorization': 'Bearer token'
            }))
        )

    @mock.patch('requests.get')
    def test_get_data_set(self, mock_get):
        mock_get.__name__ = 'get'
        api = AdminAPI('http://admin.api', 'token')
        api.get_data_set('group', 'type')

        mock_get.assert_called_with(
            'http://admin.api/data-sets?data-group=group&data-type=type',
            headers=match_equality(has_entries({
                'Accept': 'application/json',
                'Authorization': 'Bearer token'
            }))
        )

    @mock.patch('requests.get')
    def test_make_sure_returns_response(self, mock_get):
        response = Response()
        response.status_code = 200
        response._content = b'[{"data-type":"type"}]'
        mock_get.return_value = response
        mock_get.__name__ = 'get'

        api = AdminAPI('http://admin.api', 'token')
        data_sets = api.list_data_sets()

        eq_(data_sets[0]['data-type'], 'type')

    @mock.patch('requests.get')
    def test_dry_run(self, mock_get):
        api = AdminAPI('http://admin.api', 'token', dry_run=True)
        api.list_data_sets()

        eq_(mock_get.called, False)

    @mock.patch('requests.get')
    def test_returns_None_on_404(self, mock_get):
        response = Response()
        response.status_code = 404
        mock_get.return_value = response
        mock_get.__name__ = 'get'

        api = AdminAPI('http://admin.api', 'token')
        data_sets = api.list_data_sets()

        eq_(data_sets, None)

    @mock.patch('requests.get')
    def test_get_data_set_should_only_return_one(self, mock_get):
        response = Response()
        response.status_code = 200
        response._content = b'[{"data-type":"type"}]'
        mock_get.return_value = response
        mock_get.__name__ = 'get'

        api = AdminAPI('http://admin.api', 'token')
        data_set = api.get_data_set('foo', 'type')

        eq_(data_set['data-type'], 'type')

    @mock.patch('requests.get')
    def test_get_data_set_should_return_None_if_no_match(self, mock_get):
        response = Response()
        response.status_code = 200
        response._content = b'[]'
        mock_get.return_value = response
        mock_get.__name__ = 'get'

        api = AdminAPI('http://admin.api', 'token')
        data_set = api.get_data_set('foo', 'type')

        eq_(data_set, None)

    @mock.patch('requests.get')
    def test_get_data_set_should_still_return_None(self, mock_get):
        response = Response()
        response.status_code = 404
        mock_get.return_value = response
        mock_get.__name__ = 'get'

        api = AdminAPI('http://admin.api', 'token')
        data_set = api.get_data_set('foo', 'bar')

        eq_(data_set, None)

    @mock.patch('time.sleep')
    @mock.patch('requests.get')
    def test_backs_off_on_bad_gateway(self, mock_get, mock_sleep):
        good = Response()
        good.status_code = 200
        good._content = "[]"
        bad = Response()
        bad.status_code = 502

        mock_get.side_effect = [bad, bad, good]
        mock_get.__name__ = 'get'

        api = AdminAPI('http://admin.api', 'token')
        api.list_data_sets()

        eq_(mock_get.call_count, 3)
