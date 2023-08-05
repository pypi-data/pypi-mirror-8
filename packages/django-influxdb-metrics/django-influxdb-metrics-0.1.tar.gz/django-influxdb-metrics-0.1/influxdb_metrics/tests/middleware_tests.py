"""Tests for the middlewares of the influxdb_metrics app."""
from django.test import TestCase, RequestFactory

from mock import patch

from ..middleware import InfluxDBRequestMiddleware


class InfluxDBRequestMiddlewareTestCase(TestCase):
    """Tests for the ``InfluxDBRequestMiddleware`` middleware."""
    longMessage = True

    def setUp(self):
        self.patch_write_points = patch(
            'influxdb_metrics.middleware.write_points')
        self.mock_write_points = self.patch_write_points.start()

    def tearDown(self):
        self.patch_write_points.stop()

    def test_middleware(self):
        req = RequestFactory().get('/')
        req.META['HTTP_REFERER'] = 'http://google.co.uk/foobar/'
        mware = InfluxDBRequestMiddleware()
        mware.process_view(req, 'view_funx', 'view_args', 'view_kwargs')
        mware.process_exception(req, None)
        self.assertEqual(
            self.mock_write_points.call_args[0][0][0]['points'][0][6],
            'google.co.uk',
            msg=('Should correctly determine referer_tld'))

        req = RequestFactory().get('/')
        req.META['HTTP_REFERER'] = 'http://google.co.uk/foobar/'
        mware = InfluxDBRequestMiddleware()
        mware.process_view(req, 'view_funx', 'view_args', 'view_kwargs')
        mware.process_response(req, None)
        self.assertEqual(
            self.mock_write_points.call_args[0][0][0]['points'][0][6],
            'google.co.uk',
            msg=('Should also work for successful responses'))

        req = RequestFactory().get('/', HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        req.META['HTTP_REFERER'] = 'http://google.co.uk/foobar/'
        mware = InfluxDBRequestMiddleware()
        mware.process_view(req, 'view_funx', 'view_args', 'view_kwargs')
        mware.process_response(req, None)
        self.assertEqual(
            self.mock_write_points.call_args[0][0][0]['points'][0][6],
            'google.co.uk',
            msg=('Should also work for ajax requests'))
