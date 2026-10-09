"""
Lecture des logs CloudWatch /bricoshop/app en ne gardant que les ERREURS.
Affiche 10 lignes contenant "ERROR" pour verifier le filtrage.

Prerequis :
    pip install boto3 python-dotenv

Identifiants necessaires dans le fichier .env (IAM, PAS la cle Bedrock) :
    AWS_ACCESS_KEY_ID=...
    AWS_SECRET_ACCESS_KEY=...
    AWS_REGION=eu-west-1        # la region du log group

Lancer :
    python read_errors.py
"""

import time
import datetime
from dotenv import load_dotenv
import boto3

load_dotenv()

# --- Parametres ---
LOG_GROUP = "/bricoshop/app"   # le groupe de logs a lire
HOURS_BACK = 24                # fenetre de temps : dernieres 24 h
NB_LIGNES = 10                 # combien de lignes d'erreur afficher
FILTRE = "ERROR"               # ne garder que les lignes contenant ce mot

# Le client "logs" utilise AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY / AWS_REGION
logs = boto3.client("logs")

start_time_ms = int((time.time() - HOURS_BACK * 3600) * 1000)

print(f"Recherche des lignes '{FILTRE}' dans {LOG_GROUP} (dernieres {HOURS_BACK} h)...\n")

resp = logs.filter_log_events(
    logGroupName=LOG_GROUP,
    startTime=start_time_ms,
    filterPattern=FILTRE,      # filtrage cote CloudWatch : plus rapide, moins de donnees
    limit=NB_LIGNES,
)

events = resp.get("events", [])

if not events:
    print(f"Aucune ligne contenant '{FILTRE}' sur cette periode.")
    print("-> Essaie d'augmenter HOURS_BACK, ou verifie la casse du mot (ERROR vs Error).")
else:
    print(f"=== {len(events)} lignes en erreur ===\n")
    for e in events:
        horodatage = datetime.datetime.fromtimestamp(e["timestamp"] / 1000)
        print(f"[{horodatage:%Y-%m-%d %H:%M:%S}] {e['message'].rstrip()}")
