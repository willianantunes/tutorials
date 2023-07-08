from django.test import TestCase
from django.urls import reverse


class ViewsTestCase(TestCase):
    def test_should_execute_http_call(self):
        endpoint = reverse("view-http-call")
        response = self.client.get(endpoint)
        self.assertEquals(200, response.status_code)
        body = response.json()
        self.assertTrue(body.get("character") and body.get("movie"))

    def test_should_call_route_that_executes_10_http_calls_gevent(self):
        endpoint = reverse("view-http-call-10-g")
        response = self.client.get(endpoint)
        self.assertEquals(200, response.status_code)
        body = response.json()
        self.assertTrue(body.get("recommendations") and len(body["recommendations"]) == 10)

    def test_should_execute_database_call(self):
        endpoint = reverse("view-database-call")
        response = self.client.get(endpoint)
        self.assertEquals(200, response.status_code)

    def test_should_execute_http_and_database_calls(self):
        endpoint = reverse("view-http-and-database-calls")
        response = self.client.get(endpoint)
        self.assertEquals(200, response.status_code)
