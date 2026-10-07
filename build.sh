#!/usr/bin/env bash
# Arrête le script immédiatement en cas d'erreur
set -o errexit

# 1. Installer toutes les dépendances Python (dj-database-url, boto3, django-storages, etc.)
pip install -r requirements.txt

# 2. Rassembler les fichiers statiques (CSS, JS) pour WhiteNoise
python manage.py collectstatic --no-input

# 3. Appliquer les migrations de modèles directement sur la base de données Supabase
python manage.py migrate



# Forcer la création du superutilisateur lors du déploiement
DJANGO_SUPERUSER_PASSWORD="CFMA_1_2026!" python manage.py createsuperuser --username admin1 --email cfmaci225.contact@gmail.com --no-input || true
