import unittest
from src.extraction import masquer_secrets, normaliser_log, normaliser_scan, normaliser_pipeline

class TestExtraction(unittest.TestCase):
    def test_masquer_secrets(self):
        self.assertEqual(masquer_secrets("user=bob password=abc123"), "user=bob password=[SECRET]")
        self.assertEqual(masquer_secrets("token: my_token_123; foo=bar"), "token=[SECRET]; foo=bar")