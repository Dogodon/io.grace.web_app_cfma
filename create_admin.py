import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Utilise le modèle utilisateur configuré dans Django
from django.contrib.auth import get_user_model
User = get_user_model()

def run():
    username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
    email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@cfma.com')
    password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

    if not username or not password:
        print("⚠️ Les variables d'environnement ADMIN_USERNAME ou ADMIN_PASSWORD sont manquantes.")
        return

    # Nettoyage de l'ancien compte pour éviter les conflits
    User.objects.filter(username=username).delete()

    # Création propre avec les pleins pouvoirs
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    print(f"🎉 SUCCÈS : L'administrateur '{username}' a été créé avec les privilèges globaux.")

if __name__ == '__main__':
    run()
