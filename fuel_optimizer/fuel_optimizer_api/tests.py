# fuel_optimizer_api/tests.py

from django.test import TestCase
from django.urls import reverse

class OptimizeRouteTests(TestCase):
    def test_optimize_route(self):
        response = self.client.get(reverse('optimize_route'), {'start_location': '34.052235,-118.243683', 'finish_location': '40.712776,-74.005974'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('route', response.json())
        self.assertIn('optimal_stops', response.json())
        self.assertIn('total_cost', response.json())
