from src.contrat import Analyse, Evenement

def est_doublon(evt: Evenement, vus: set) -> bool:
    raise NotImplementedError

def compter_erreurs(evt: Evenement, compteur: dict) -> int:
    raise NotImplementedError

def chercher_procedures(evt: Evenement, base: dict) -> list:
    message = evt.message.lower()
    resultats = []

    for nom, procedure in base.items():
        if isinstance(procedure, dict):
            mots_cles = procedure.get("mots_cles", [])
        else:
            mots_cles = [nom]

        if isinstance(mots_cles, str):
            mots_cles = [mots_cles]

        if any(mot.lower() in message for mot in mots_cles):
            resultats.append(procedure)

    return resultats


def classifier(evt: Evenement, nb_erreurs: int = 0) -> str:
    if nb_erreurs >= 3:
        return "CRITICAL"

    if evt.severity == "CRITICAL":
        return "CRITICAL"

    if nb_erreurs >= 2:
        return "HIGH"

    if evt.severity == "HIGH":
        return "HIGH"

    return evt.severity


def analyser(evt: Evenement, base: dict, nb_erreurs: int = 0) -> Analyse:
    procedures = chercher_procedures(evt, base)
    niveau = classifier(evt, nb_erreurs)

    # La construction dépend des champs définis dans src/contrat.py.
    return Analyse(
        evenement=evt,
        niveau=niveau,
        procedures=procedures,
    )

def analyser(evt: Evenement, base: dict, nb_erreurs: int = 0) -> Analyse:
    raise NotImplementedError