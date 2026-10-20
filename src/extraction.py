import re
from src.contrat import Evenement

def masquer_secrets(texte: str) -> str:
    pattern = re.compile(r'\b(password|passwd|token|secret|api_key|apikey)\s*[=:]\s*[^ &;,]+', re.IGNORECASE)
    return pattern.sub(r'\1=[SECRET]', texte)

def normaliser_log(ligne: str, numero: int, source: str = "DOCKER",
environment: str = "production") -> Evenement:
    raise NotImplementedError
def normaliser_scan(rapport: dict, numero: int,
environment: str = "production") -> Evenement:
    raise NotImplementedError

def normaliser_pipeline(rapport: dict, numero: int,
environment: str = "production") -> Evenement:
    raise NotImplementedError