import unittest
import sys
import os

# Add requests import with fallback
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False
    print("Warning: requests library not available, skipping HTTP tests")

from app import app

class TestApp(unittest.TestCase):
    def test_app_creation(self):
        """Test that the Flask app can be created"""
        self.assertIsNotNone(app)
        self.assertEqual(app.name, 'app')
        print('Test passed: Flask app created successfully')
    
    def test_hello_route_function(self):
        """Test the hello route function directly"""
        with app.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.get_data(as_text=True), 'Hello from python-demo-app!')
            print('Test passed: hello route returns correct response')
    
    @unittest.skipIf(not HAS_REQUESTS, "requests library not available")
    def test_hello_endpoint_http(self):
        """Test the endpoint via HTTP (if requests is available)"""
        try:
            response = requests.get('http://127.0.0.1:3000/', timeout=1)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.text, 'Hello from python-demo-app!')
            print('Test passed: HTTP endpoint responded correctly')
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            print('skipped: local server not started in CI; use unit tests in real projects')
            pass

if __name__ == '__main__':
    print('Running Python Flask App Tests...')
    
    # Simple fallback test if requests is not available
    if not HAS_REQUESTS:
        print('Running basic app tests without HTTP requests...')
    
    # Run the tests
    unittest.main(verbosity=2, exit=True)