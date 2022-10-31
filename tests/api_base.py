
import unittest
from unittest.mock import Mock
from app import app
from utilities.test_helpers import inject_mock_middleware, inject_test_dependency
from framework.clients.feature_client import FeatureClient
from framework.clients.cache_client import CacheClient


class ApiTest(unittest.TestCase):
    def setUp(self) -> None:
        self.mock_feature_client = Mock()
        self.mock_cache_client = Mock()

        inject_test_dependency(
            _type=FeatureClient,
            instance=self.mock_feature_client)
        inject_test_dependency(
            _type=CacheClient,
            instance=self.mock_cache_client)

        inject_mock_middleware()

    def _get_mock_auth_headers(self):
        return {
            'Authorization': 'Bearer fake',
            'Content-Type': 'application/json'
        }

    def send_request(self, method, endpoint,  headers=None, json=None, request_args=None):
        with app.test_client() as client:
            _headers = (headers or {}) | self._get_mock_auth_headers()
            return client.open(
                endpoint,
                method=method,
                headers=_headers,
                json=json,
                query_string=request_args or {})
