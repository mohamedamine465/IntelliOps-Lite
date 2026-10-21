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

    def test_normaliser_scan(self):
        rap = {"cve": "CVE-123", "package": "lib", "severity": "critical", "date": "2026-10-05T10:07:00Z"}
        evt = normaliser_scan(rap, 1)
        self.assertEqual(evt.event_type, "VULNERABILITY")
        self.assertEqual(evt.severity, "CRITICAL")
        self.assertEqual(evt.message, "Vulnerabilite CVE-123 dans lib")

    def test_normaliser_pipeline(self):
        rap = {"job": "build", "status": "failed", "date": "2026-10-05T10:06:00Z"}
        evt = normaliser_pipeline(rap, 2)
        self.assertEqual(evt.event_type, "PIPELINE_FAILURE")
        self.assertEqual(evt.severity, "HIGH")
    def test_bearer(self):
        self.assertEqual(masquer_secrets("Authorization: Bearer eyJ.abc-1"),
                     "Authorization: Bearer [SECRET]")

if __name__ == '__main__':
    unittest.main()