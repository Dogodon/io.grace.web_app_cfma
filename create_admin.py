import os
import django

# Initialisation de l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from cfma_base.models import User  # Ajustez l'import selon l'emplacement exact de votre modèle User

def run():
    username = "secretaire-cfma-ci-s"
    email = "secretaire@cfma.com"
    password = "VOTRE_MOT_DE_PASSE_ICI"  # <--- METTEZ VOTRE VRAI MOT DE PASSE ICI

    # Supprime l'ancien compte s'il existe et n'a pas les droits pour éviter les conflits
    User.objects.filter(username=username).delete()

    # Création du compte avec les droits d'administration totaux
    user = User.objects.create_user(
        username=username,
        email=email,
        password=password
    )
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print("=== LE COMPTE ADMIN A ÉTÉ FORCÉ AVEC SUCCÈS ===")

if __name__ == '__main__':
    run()
