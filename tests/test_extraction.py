import unittest
from src.extraction import masquer_secrets, normaliser_log, normaliser_scan, normaliser_pipeline

class TestExtraction(unittest.TestCase):
    def test_masquer_secrets(self):
        self.assertEqual(masquer_secrets("user=bob password=abc123"), "user=bob password=[SECRET]")
        self.assertEqual(masquer_secrets("token: my_token_123; foo=bar"), "token=[SECRET]; foo=bar")

def test_normaliser_log(self):
        ligne = "2026-10-05 10:02:11 ERROR backend OOMKilled restarts=14 password=abc123"
        evt = normaliser_log(ligne, 42)
        self.assertEqual(evt.id, "EVT-00042")
        self.assertEqual(evt.timestamp, "2026-10-05T10:02:11Z")
        self.assertEqual(evt.severity, "HIGH")
        self.assertNotIn("abc123", evt.message)