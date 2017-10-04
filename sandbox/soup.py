import os
import unittest
import requests
from bs4 import BeautifulSoup

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(__file__), p))

portal_url = "http://alpha.esihs.net/portal"
source = requests.get(portal_url).text
soup = BeautifulSoup(source, 'html.parser')
items = soup.find_all()


class AppTests(unittest.TestCase):

    def test_add_items(self):
        for item in items:
            # if 'id' in item.attrs and item.attrs['id'] == 'loginBtn':
            if 'id' in item.attrs and 'value' in item.attrs:
                print item.name, item.attrs['id'] + ': ' + item.attrs['value']


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(AppTests)
    unittest.TextTestRunner(verbosity=2).run(suite)
