# Workshop — Amazon Bedrock + CloudWatch avec Python

Analyser les logs d'une application (CloudWatch) avec un modèle d'IA
(**Ministral 14B 3.0** sur Amazon Bedrock), en Python.

---

## Contenu du projet

| Fichier | Rôle |
|---|---|
| `setup-bedrock.ps1` | Script d'installation de l'environnement Python (Windows) |
| `.env.example` | Modèle de configuration (sans secrets) à copier en `.env` |
| `bedrock_mistral.py` | Premier appel au modèle (test « hello world ») |
| `bedrock_assistant.py` | Appel configurable (prompt système, température, tokens) |
| `read_logs.py` | Lit 10 lignes de logs depuis CloudWatch |
| `read_errors.py` | Lit 10 lignes contenant `ERROR` |
| `analyze_error.py` | Récupère la 1ʳᵉ erreur et demande son analyse à Ministral |

---

## Prérequis

- Python 3.10+
- Un compte AWS avec :
  - l'accès au modèle **Ministral 14B 3.0** activé dans Bedrock (*Model access*)
  - des identifiants IAM pouvant lire CloudWatch Logs

---

## Étape 1 — Installer l'environnement Python

Dans PowerShell, depuis le dossier du projet :

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install boto3 python-dotenv
```

> Ton invite doit afficher `(.venv)` au début = environnement activé.
> Si l'activation est bloquée : `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass`
>
> Raccourci : le script `setup-bedrock.ps1` fait l'installation à ta place.

---

## Étape 2 — Créer le fichier `.env`

Copie le modèle puis remplis les vraies valeurs :

```powershell
copy .env.example .env
```

Ouvre `.env` et renseigne :

```dotenv
# Clé API Bedrock (console Bedrock > "Generate short-term API key")
AWS_BEARER_TOKEN_BEDROCK=ta_cle_bedrock

# Identifiants IAM pour lire CloudWatch Logs
AWS_ACCESS_KEY_ID=ta_access_key
AWS_SECRET_ACCESS_KEY=ta_secret_key

# Région AWS (celle du modèle Bedrock ET du log group CloudWatch)
AWS_REGION=eu-west-1
```

> ⚠️ **Deux authentifications différentes :**
> - `AWS_BEARER_TOKEN_BEDROCK` → sert **uniquement** à Bedrock (le modèle IA).
> - `AWS_ACCESS_KEY_ID` + `AWS_SECRET_ACCESS_KEY` → servent à lire **CloudWatch Logs**.
>
> 🔒 Le fichier `.env` ne doit **jamais** être poussé sur Git (déjà exclu par `.gitignore`).

---

## Étape 3 — Tester l'accès au modèle

```powershell
python bedrock_mistral.py
```

Si tu obtiens une réponse du modèle, Bedrock fonctionne. ✅
Erreur `AccessDeniedException` ? → active l'accès au modèle dans la console Bedrock (*Model access*) pour ta région.

---

## Étape 4 — Tester la lecture des logs

```powershell
python read_logs.py      # 10 dernières lignes de logs
python read_errors.py    # 10 lignes contenant ERROR
```

Si tu obtiens des lignes, CloudWatch fonctionne. ✅
`Aucun log trouvé` ? → vérifie **la région** et le **nom du log group** (`/bricoshop/app`).
`AccessDenied` ? → vérifie les permissions IAM (`logs:FilterLogEvents`...).

---

## Étape 5 — Analyser une erreur avec l'IA

Le script complet : il récupère la première erreur des logs et demande
son analyse à Ministral (rôle : expert DevOps & dev web).

```powershell
python analyze_error.py
```

---

## Étape 6 — Personnaliser

Dans `bedrock_assistant.py` et `analyze_error.py`, tu peux régler :

- `SYSTEM_PROMPT` — le rôle / les consignes du modèle
- `TEMPERATURE` — `0.0` = factuel et stable, `1.0` = plus créatif
- `MAX_TOKENS` — longueur maximale de la réponse
- `USER_PROMPT` — la question posée

Dans `read_logs.py` / `read_errors.py` :

- `LOG_GROUP` — le groupe de logs à lire
- `HOURS_BACK` — fenêtre de temps (en heures)
- `FILTRE` — le mot-clé filtré (sensible à la casse : `ERROR` ≠ `Error`)

---

## Dépannage rapide

| Symptôme | Cause probable |
|---|---|
| `AccessDeniedException` sur Bedrock | accès au modèle non activé pour la région |
| `AccessDenied` sur les logs | permissions IAM insuffisantes |
| `Aucun log trouvé` | mauvaise région, mauvais log group, ou fenêtre trop courte |
| Clé Bedrock expirée | la clé court-terme dure ~12 h → regénère-la |
| `.env` apparaît dans `git status` | ne pas committer ; vérifier le `.gitignore` |
