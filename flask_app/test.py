import unittest
from main import (log, load_data, log_statistics, find_ifsc, get_bank_leader_board, statistics)
from main import app, load_data
import config

class TestFlaskApis(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.headers = {"Content-Type": "application/json"}

    def test_ifsc_search(self):
        url = '/ifsc_search?ifsc_code=ABHY0065001'

        load_data(config.path)
        response = self.app.get(url, headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_bank_leader_board(self):
        url = '/bank_leader_board'

        load_data(config.path)
        response = self.app.get(url, headers=self.headers)

        self.assertEqual(response.status_code, 200)

    def test_statistics(self):
        url = '/ifsc_search?ifsc_code=ABHY0065001'
        load_data(config.path)
        response = self.app.get(url, headers=self.headers)
        if response.status_code == 200:
            url_statistics = '/statistics'
            resp = self.app.get(url_statistics, headers=self.headers)

            self.assertEqual(resp.status_code, 200)


if __name__ == '__main__':
    unittest.main()
