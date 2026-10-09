"""
Test de lecture des logs CloudWatch du log group /bricoshop/app.
Objectif : verifier que la connexion + les permissions marchent
en affichant simplement 10 lignes de logs.

Prerequis :
    pip install boto3 python-dotenv

Identifiants necessaires dans le fichier .env (IAM, PAS la cle Bedrock) :
    AWS_ACCESS_KEY_ID=...
    AWS_SECRET_ACCESS_KEY=...
    AWS_REGION=eu-west-1        # la region du log group

Lancer :
    python read_logs.py
"""

import time
import datetime
from dotenv import load_dotenv
import boto3

load_dotenv()

# --- Parametres ---
LOG_GROUP = "/bricoshop/app"   # le groupe de logs a lire
HOURS_BACK = 24                # fenetre de temps : dernieres 24 h
NB_LIGNES = 10                 # combien de lignes afficher

# Le client "logs" utilise AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY / AWS_REGION
logs = boto3.client("logs")

start_time_ms = int((time.time() - HOURS_BACK * 3600) * 1000)

print(f"Lecture de {LOG_GROUP} (dernieres {HOURS_BACK} h)...\n")

resp = logs.filter_log_events(
    logGroupName=LOG_GROUP,
    startTime=start_time_ms,
    limit=NB_LIGNES,
)

events = resp.get("events", [])

if not events:
    print("Aucun log trouve sur cette periode.")
    print("-> Verifie le nom du log group, la region, et la fenetre de temps (HOURS_BACK).")
else:
    print(f"=== {len(events)} lignes de logs ===\n")
    for e in events:
        # timestamp CloudWatch = millisecondes depuis epoch
        horodatage = datetime.datetime.fromtimestamp(e["timestamp"] / 1000)
        print(f"[{horodatage:%Y-%m-%d %H:%M:%S}] {e['message'].rstrip()}")
