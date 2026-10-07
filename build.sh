#!/usr/bin/env bash
# Arrête le script immédiatement en cas d'erreur
set -o errexit

# 1. Installer toutes les dépendances Python (dj-database-url, boto3, django-storages, etc.)
pip install -r requirements.txt

# 2. Rassembler les fichiers statiques (CSS, JS) pour WhiteNoise
python manage.py collectstatic --no-input

# 3. Appliquer les migrations de modèles directement sur la base de données Supabase
python manage.py migrate
