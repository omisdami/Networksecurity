import unittest
from app import app  # Importing the Flask app instance

class AppTestCase(unittest.TestCase):
    def setUp(self):
        """Set up a test client for the Flask app."""
        self.app = app.test_client()
        self.app.testing = True

    def test_home(self):
        """Test if the home route returns 'Hello World!'"""
        response = self.app.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode("utf-8"), "Hello World!")

if __name__ == "__main__":
    unittest.main()