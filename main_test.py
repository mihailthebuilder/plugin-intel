import unittest
from main import extract_path


class TestExtractPath(unittest.TestCase):

    def test_happy_path(self):
        got = "https://workspace.google.com/marketplace/app/facebook_ads_instagram_data_meta_by_sync/525820101725"
        expected = "facebook_ads_instagram_data_meta_by_sync/525820101725"
        self.assertEqual(extract_path(got), expected)
