from tests.api_base import ApiTest


class HealthTests(ApiTest):
    def test_get_alive(self):
        result = self.send_request(
            endpoint='/api/health/alive',
            method='GET')

        self.assertEqual(200, result.status_code)

    def test_get_ready(self):
        result = self.send_request(
            endpoint='/api/health/ready',
            method='GET')

        self.assertEqual(200, result.status_code)
