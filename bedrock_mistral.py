"""
Premier appel a Amazon Bedrock avec un modele Mistral.
Utilise la cle API Bedrock (AWS_BEARER_TOKEN_BEDROCK) lue depuis le fichier .env.

Prerequis :
    pip install boto3 python-dotenv

Lancer :
    python bedrock_mistral.py
"""

import os
from dotenv import load_dotenv
import boto3

# 1. Charger les variables du fichier .env dans l'environnement.
#    boto3 lit AWS_BEARER_TOKEN_BEDROCK tout seul : pas besoin de le passer en argument.
load_dotenv()

REGION = os.getenv("AWS_REGION", "eu-west-1")

# 2. Choisir le modele.
#    Ministral 14B 3.0 -> supporte l'API Converse, dispo in-region en eu-west-1.
#    -> L'acces au modele doit etre active dans la console Bedrock
#       (Amazon Bedrock > Model access) pour la region ci-dessus.
#    Autres identifiants possibles :
#       mistral.ministral-3-8b-instruct
#       mistral.mistral-large-2407-v1:0
MODEL_ID = "mistral.ministral-3-14b-instruct"

# 3. Creer le client bedrock-runtime (c'est lui qui fait les appels aux modeles).
client = boto3.client("bedrock-runtime", region_name=REGION)

# 4. Envoyer un message avec l'API "Converse" (format unifie, simple a utiliser).
response = client.converse(
    modelId=MODEL_ID,
    messages=[
        {
            "role": "user",
            "content": [{"text": "Salut, quel est la capitale de la France ?"}],
        }
    ],
    inferenceConfig={"maxTokens": 300, "temperature": 0.7},
)

# 5. Afficher la reponse.
texte = response["output"]["message"]["content"][0]["text"]
print("\n=== Reponse du modele ===\n")
print(texte)
