import unittest
from src.analyse import analyser, classifier, compter_erreurs, est_doublon, chercher_procedures
from src.contrat import PROCEDURES, Evenement

def evt(type_="LOG", severity="HIGH", message="OOMKilled restarts=14", composant="backend"):
    return Evenement("EVT-00001", "2026-10-05T10:00:00Z", "DOCKER", composant, "production", type_, severity, message, "NEW")

class TestAnalyse(unittest.TestCase):
    def test_doublon(self):
        vus = set()
        self.assertFalse(est_doublon(evt(), vus))
        self.assertTrue(est_doublon(evt(), vus))

    def test_classifier_boucle(self):
        e = evt()
        self.assertEqual(classifier(e, 3), "CRITICAL")
        self.assertEqual(classifier(e, 2), "HIGH")
        
    def test_compter_erreurs(self):
        compteur = {}
        e = evt()
        self.assertEqual(compter_erreurs(e, compteur), 1)
        self.assertEqual(compter_erreurs(e, compteur), 2)

    def test_analyser(self):
        base = {"oomkilled": "Augmenter la limite memoire."}
        e = evt()
        a = analyser(e, base, 3)
        self.assertEqual(a.level, "CRITICAL")
        self.assertEqual(a.action, "Redemarrer le service backend")
        self.assertTrue(a.sensitive)

if __name__ == "__main__":
    unittest.main()