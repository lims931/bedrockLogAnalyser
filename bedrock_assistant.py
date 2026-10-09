"""
Appel configurable a Amazon Bedrock (Ministral 14B 3.0) via l'API Converse.

Tout ce que tu peux regler est regroupe dans la section CONFIGURATION ci-dessous :
    - SYSTEM_PROMPT : le role / les consignes donnees au modele
    - MAX_TOKENS    : longueur max de la reponse (le "token")
    - TEMPERATURE   : creativite (0 = factuel/stable, 1 = plus varie)
    - USER_PROMPT   : la question / demande de l'utilisateur

Prerequis :
    pip install boto3 python-dotenv

Lancer :
    python bedrock_assistant.py
"""

import os
from dotenv import load_dotenv
import boto3

load_dotenv()

REGION = os.getenv("AWS_REGION", "eu-west-1")
MODEL_ID = "mistral.ministral-3-14b-instruct"

# ============================================================
#  CONFIGURATION  -  c'est ici que tu modifies tout
# ============================================================

# --- Prompt systeme : qui est le modele, comment il doit repondre ---
SYSTEM_PROMPT = """Tu es un assistant DevOps senior.
Tu analyses les messages d'erreur et les logs, tu expliques la cause probable
en termes simples, puis tu proposes une solution concrete avec les commandes a executer.
Reponds toujours en francais, de maniere concise et structuree."""

# --- Longueur max de la reponse (en tokens) ---
MAX_TOKENS = 600

# --- Temperature : 0.0 = reponses stables/factuelles, 1.0 = plus creatives ---
TEMPERATURE = 0.3

# --- Prompt utilisateur : la demande concrete ---
USER_PROMPT = """J'ai cette erreur quand je lance mon conteneur :

docker: Error response from daemon: driver failed programming external
connectivity on endpoint web: Bind for 0.0.0.0:8080 failed: port is already allocated.

Explique-moi ce qui se passe et comment le corriger."""

# ============================================================
#  APPEL DU MODELE  -  en general tu ne touches pas a ce bloc
# ============================================================

client = boto3.client("bedrock-runtime", region_name=REGION)

response = client.converse(
    modelId=MODEL_ID,
    system=[{"text": SYSTEM_PROMPT}],
    messages=[
        {
            "role": "user",
            "content": [{"text": USER_PROMPT}],
        }
    ],
    inferenceConfig={
        "maxTokens": MAX_TOKENS,
        "temperature": TEMPERATURE,
    },
)

texte = response["output"]["message"]["content"][0]["text"]
usage = response.get("usage", {})

print("\n=== Reponse du modele ===\n")
print(texte)
print("\n--- Tokens utilises ---")
print(f"entree : {usage.get('inputTokens')}  |  "
      f"sortie : {usage.get('outputTokens')}  |  "
      f"total : {usage.get('totalTokens')}")
