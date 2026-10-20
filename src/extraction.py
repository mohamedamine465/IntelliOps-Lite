import re
from src.contrat import Evenement

def masquer_secrets(texte: str) -> str:
    pattern = re.compile(r'\b(password|passwd|token|secret|api_key|apikey)\s*[=:]\s*[^ &;,]+', re.IGNORECASE)
    return pattern.sub(r'\1=[SECRET]', texte)

def normaliser_log(ligne: str, numero: int, source: str = "DOCKER", environment: str = "production") -> Evenement:
    parts = ligne.split(maxsplit=4)
    if len(parts) < 5:
        raise ValueError("Ligne mal formée")
    
    date, time, niveau, composant, reste = parts
    timestamp = f"{date}T{time}Z"
    niveau_up = niveau.upper()
    
    if niveau_up in ["CRITICAL", "FATAL"]: 
        sev = "CRITICAL"
    elif niveau_up == "ERROR": 
        sev = "HIGH"
    elif niveau_up in ["WARN", "WARNING"]: 
        sev = "MEDIUM"
    else: 
        sev = "LOW"
        
    msg = masquer_secrets(reste)
    return Evenement(f"EVT-{numero:05d}", timestamp, source, composant, environment, "LOG", sev, msg, "NEW")

def normaliser_scan(rapport: dict, numero: int,
environment: str = "production") -> Evenement:
    raise NotImplementedError

def normaliser_pipeline(rapport: dict, numero: int,
environment: str = "production") -> Evenement:
    raise NotImplementedError