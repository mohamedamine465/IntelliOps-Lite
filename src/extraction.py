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

def normaliser_scan(rapport: dict, numero: int, environment: str = "production") -> Evenement:
    for k in ["cve", "package", "severity", "date"]:
        if k not in rapport: 
            raise ValueError(f"Clé manquante: {k}")
    
    sev = rapport["severity"].upper()
    if sev not in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]: 
        sev = "LOW"
        
    msg = f"Vulnerabilite {rapport['cve']} dans {rapport['package']}"
    return Evenement(f"EVT-{numero:05d}", rapport["date"], "TRIVY", rapport["package"], environment, "VULNERABILITY", sev, msg, "NEW")

def normaliser_pipeline(rapport: dict, numero: int, environment: str = "production") -> Evenement:
    for k in ["job", "status", "date"]:
        if k not in rapport: 
            raise ValueError(f"Clé manquante: {k}")
            
    status = rapport["status"].lower()
    if status == "failed":
        event_type = "PIPELINE_FAILURE"
        sev = "HIGH"
    else:
        event_type = "PIPELINE_OK"
        sev = "LOW"
        
    msg = f"Pipeline {rapport['job']}: {rapport['status']}"
    return Evenement(f"EVT-{numero:05d}", rapport["date"], "CI", rapport["job"], environment, event_type, sev, msg, "NEW")