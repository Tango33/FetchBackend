import unittest
from points_api import app, transactions, balance  # Adjust this import based on your directory structure

class TestPointsAPI(unittest.TestCase):
    def setUp(self):
        """
        Set up the testing client and reset global variables.
        """
        self.app = app
        self.app.testing = True  # Ensure we're in testing mode
        self.client = self.app.test_client()
        transactions.clear()
        balance.clear()

    def test_add_points(self):
        """
        Test adding points to the system.
        """
        response = self.client.post('/add', json={"payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z"})
        self.assertEqual(response.status_code, 200)

    def test_spend_points(self):
        """
        Test spending points from the system.
        """
        # First, add some points
        self.client.post('/add', json={"payer": "DANNON", "points": 300, "timestamp": "2022-10-31T10:00:00Z"})
        response = self.client.post('/spend', json={"points": 200})
        self.assertEqual(response.status_code, 200)

    def test_balance(self):
        """
        Test fetching the balance from the system.
        """
        response = self.client.get('/balance')
        self.assertEqual(response.status_code, 200)

    def test_insufficient_points(self):
        """
        Test trying to spend more points than available.
        """
        response = self.client.post('/spend', json={"points": 2000})
        self.assertEqual(response.status_code, 400)


if __name__ == "__main__":
    unittest.main()
