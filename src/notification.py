from src.contrat import Analyse, Evenement, Notification

def choisir_canal(niveau: str) -> str:
    canaux = {
        "CRITICAL": "TEAMS",
        "HIGH": "SLACK",
        "MEDIUM": "EMAIL",
        "LOW": "DASHBOARD"
    }
    if niveau not in canaux:
        raise ValueError(f"Niveau non reconnu : {niveau}")
    return canaux[niveau]

def rediger(evt: Evenement, analyse: Analyse) -> str:
    sources_str = ", ".join(analyse.sources)
    return (
        f"[{analyse.level}] Composant : {evt.component}\n"
        f"Evenement : {evt.message}\n"
        f"Explication : {analyse.explanation}\n"
        f"Action proposee : {analyse.action}\n"
        f"Sources : {sources_str}"
    )

def notifier(evt: Evenement, analyse: Analyse, historique: list) -> Notification:
    raise NotImplementedError

def valider_action(analyse: Analyse, reponse: str) -> bool:
    if not analyse.sensitive:
        return True
    # Nettoyage de la réponse : on enlève les espaces et on met en minuscules
    rep = reponse.strip().lower()
    return rep in ["o", "oui", "ok", "yes"]

def tracer_decision(analyse: Analyse, approuve: bool, acteur: str,
    journal: list, horodatage: str) -> dict:
    raise NotImplementedError