# ============================================================
#  Setup environnement Python pour Amazon Bedrock (Windows)
#  A executer dans PowerShell, depuis le dossier du projet.
#  Lancer les commandes une par une, OU le script entier :
#     .\setup-bedrock.ps1
# ============================================================

# --- 0. (si besoin) autoriser l'activation du venv pour CETTE session ---
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force

# --- 1. Creer l'environnement virtuel ---
python -m venv .venv

# --- 2. Activer le venv (ton invite doit afficher "(.venv)") ---
.\.venv\Scripts\Activate.ps1

# --- 3. Mettre pip a jour ---
python -m pip install --upgrade pip

# --- 4. Installer les dependances ---
# boto3 suffit pour parler a Bedrock en Python.
# awscli est optionnel (sert a "aws configure") et cause parfois
# des conflits de versions -> ne l'installe que si tu en as besoin.
pip install boto3
# pip install awscli      # <- decommente seulement si tu veux la CLI AWS

# --- 5. Verifier l'installation ---
python -c "import boto3; print('boto3', boto3.__version__)"

Write-Host ""
Write-Host "OK : environnement pret. Pense a configurer tes identifiants AWS :" -ForegroundColor Green
Write-Host "   aws configure            (si awscli installe)" -ForegroundColor Green
Write-Host "   ou variables d'env AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY / AWS_DEFAULT_REGION" -ForegroundColor Green
