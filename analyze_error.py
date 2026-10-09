"""
Recupere la PREMIERE erreur trouvee dans les logs CloudWatch /bricoshop/app,
puis demande son avis a Ministral (role : expert DevOps & developpeur web).

Ce script combine les DEUX services AWS, donc les DEUX authentifications :
    - CloudWatch Logs  -> identifiants IAM (AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY)
    - Bedrock (Ministral) -> cle API (AWS_BEARER_TOKEN_BEDROCK)

Prerequis :
    pip install boto3 python-dotenv

Fichier .env attendu :
    AWS_ACCESS_KEY_ID=...
    AWS_SECRET_ACCESS_KEY=...
    AWS_BEARER_TOKEN_BEDROCK=...
    AWS_REGION=eu-west-1

Lancer :
    python analyze_error.py
"""

import time
import datetime
from dotenv import load_dotenv
import boto3

load_dotenv()

# --- Parametres ---
LOG_GROUP = "/bricoshop/app"
HOURS_BACK = 24
FILTRE = "ERROR"
MODEL_ID = "mistral.ministral-3-14b-instruct"

SYSTEM_PROMPT = """Tu es un expert DevOps et developpeur web senior.
On te fournit une ligne d'erreur extraite des logs d'une application en production.
Tu dois :
1. Expliquer en termes clairs ce que signifie cette erreur.
2. Donner la ou les causes probables.
3. Proposer une solution concrete, avec les commandes ou le code a appliquer.
Reponds en francais, de maniere structuree et concise."""

# ============================================================
#  ETAPE 1 : recuperer la premiere erreur dans CloudWatch
# ============================================================

logs = boto3.client("logs")
start_time_ms = int((time.time() - HOURS_BACK * 3600) * 1000)

print(f"Recherche de la premiere erreur dans {LOG_GROUP}...\n")

resp = logs.filter_log_events(
    logGroupName=LOG_GROUP,
    startTime=start_time_ms,
    filterPattern=FILTRE,
    limit=1,                   # une seule : la premiere trouvee
)

events = resp.get("events", [])

if not events:
    print(f"Aucune ligne '{FILTRE}' trouvee sur les dernieres {HOURS_BACK} h.")
    print("-> Augmente HOURS_BACK ou verifie la casse du filtre.")
    raise SystemExit(0)

premiere_erreur = events[0]
horodatage = datetime.datetime.fromtimestamp(premiere_erreur["timestamp"] / 1000)
message_erreur = premiere_erreur["message"].rstrip()

print("=== Erreur trouvee ===")
print(f"[{horodatage:%Y-%m-%d %H:%M:%S}] {message_erreur}\n")

# ============================================================
#  ETAPE 2 : demander son avis a Ministral
# ============================================================

bedrock = boto3.client("bedrock-runtime")

user_prompt = f"""Voici une erreur extraite des logs de production :

{message_erreur}

Donne-moi ton analyse et comment la corriger."""

print("Analyse par Ministral en cours...\n")

response = bedrock.converse(
    modelId=MODEL_ID,
    system=[{"text": SYSTEM_PROMPT}],
    messages=[{"role": "user", "content": [{"text": user_prompt}]}],
    inferenceConfig={"maxTokens": 700, "temperature": 0.3},
)

avis = response["output"]["message"]["content"][0]["text"]

print("=== Avis de Ministral ===\n")
print(avis)
