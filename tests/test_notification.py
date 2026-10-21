import unittest
from src.contrat import Analyse, Evenement
from src.notification import choisir_canal, valider_action, rediger, notifier, tracer_decision

def exemple(sensible=True, niveau="CRITICAL"):
    e = Evenement("EVT-00125", "2026-10-05T10:02:11Z", "DOCKER", "backend",
                  "production", "LOG", "HIGH", "OOMKilled restarts=14")
    a = Analyse("EVT-00125", niveau, "Manque de memoire",
                "Redemarrer le service backend", sensible, ["DOCKER"])
    return e, a

class TestNotification(unittest.TestCase):
    def test_canaux(self):
        self.assertEqual(choisir_canal("CRITICAL"), "TEAMS")
        self.assertEqual(choisir_canal("LOW"), "DASHBOARD")
        with self.assertRaises(ValueError):
            choisir_canal("INCONNU")

    def test_validation(self):
        _, a = exemple(sensible=True)
        self.assertTrue(valider_action(a, " OUI "))
        self.assertTrue(valider_action(a, "ok"))
        self.assertFalse(valider_action(a, "n"))
        
        _, a_non_sensible = exemple(sensible=False)
        self.assertTrue(valider_action(a_non_sensible, "n'importe quoi"))
    def test_rediger(self):
        e, a = exemple()
        texte = rediger(e, a)
        self.assertIn("[CRITICAL] Composant : backend", texte)
        self.assertIn("Evenement : OOMKilled restarts=14", texte)
        self.assertIn("Sources : DOCKER", texte)