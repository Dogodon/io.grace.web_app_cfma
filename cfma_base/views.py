from django.shortcuts import render, redirect
from .forms import DiagnosticRDVForm

from .models import GalerieCommentaireClient # 🌟 Vérifiez l'orthographe exacte !


from .models import GalerieCommentaireClient, GalerieCommentaireEvenement, ElementService
from django.core.mail import send_mail


# 1️⃣ LA VUE D'ACCUEIL : Elle doit récupérer les données pour alimenter la boucle de l'Espace Services !
from django.shortcuts import render
from .models import GalerieCommentaireClient

from django.core.mail import send_mail, EmailMessage

from .forms import DiagnosticRDVForm 

from django.shortcuts import render, redirect
from django.core.mail import EmailMessage, get_connection
from django.contrib import messages
from django.conf import settings
from .forms import DiagnosticRDVForm 



from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
# 🌟 Importation du tout nouveau système de messagerie Django 6.1
from .forms import DiagnosticRDVForm 
from django.core.mail import send_mail





# cfma_base/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.timezone import now
from .models import MouvementVehicule
from .forms import EntreeVehiculeForm, SortieVehiculeForm
from cfma_base import views



def home(request):
    # Récupération brute des données des deux pôles
    liste_com_clients = GalerieCommentaireClient.objects.all()
    liste_com_evenements = GalerieCommentaireEvenement.objects.all()
    
    # 🎯 RECUPERATION DE VOS 7 SERVICES POUR LE CARROUSEL
    liste_services = ElementService.objects.all()
    
    context = {
        'commentaires': liste_com_clients,     # Pôle Atelier
        'evenements': liste_com_evenements,       # Pôle Événements / Académie
        'services': liste_services,               # 🎯 INJECTION INDISPENSABLE POUR LE MARQUEE !
    }
    return render(request, 'vitrine/index.html', context)

""" def home(request):
    # Récupération brute des données des deux pôles
    liste_com_clients = GalerieCommentaireClient.objects.all()
    liste_com_evenements = GalerieCommentaireEvenement.objects.all()
    
    context = {
        'commentaires': liste_com_clients, # Pôle Atelier
        'evenements': liste_com_evenements,   # Pôle Événements / Académie
    }
    return render(request, 'vitrine/index.html', context)
 """
def galeries_commentaires_clients(request):
    liste_com = GalerieCommentaireClient.objects.all()
    return render(request, 'cfma_base/galeries_commentaires_clients.html', {'commentaires': liste_com})





from django.shortcuts import render
from .models import GalerieCFMA, PartenaireContact  # 🌟 Correction du nom du modèle ici

def a_propos(request):
    # 🎯 On copie la logique qui marche : on récupère TOUTE la liste des configurations
    liste_entreprises = GalerieCFMA.objects.all()
    liste_partenaires = PartenaireContact.objects.all()
    
    context = {
        'liste_entreprises': liste_entreprises, # Renvoie la liste brute de l'admin
        'partenaires': liste_partenaires,
    }
    return render(request, 'cfma_base/a_propos.html', context)





def galeries_commentaires_evenements(request):
    # 🌟 Défini avec un 'e' : liste_com_evenements
    liste_com_evenements = GalerieCommentaireEvenement.objects.all()
    
    # 🌟 Corrigé ici aussi avec un 'e' : liste_com_evenements
    return render(request, 'cfma_base/galeries_commentaires_evenements.html', {'evenements': liste_com_evenements})



import requests
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from decouple import config

from .models import Facture, FicheTravail, StatutFacture, TransactionPaiement, TypeDocument

try:
    import pdfkit
except ImportError:
    pdfkit = None





from django.contrib.auth.decorators import user_passes_test
from .models import User, ElementService, Actualite, PartenaireContact, FormationCatalogue
from django.contrib.auth import login






from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import DiagnosticRDVForm


######################
# À ajouter dans cfma_base/views.py
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from .forms import InscriptionForm
from .models import User



class ConnexionPersonnaliseeView(LoginView):
    # Changez 'cfma_base/authentification/connexion.html' par :
    template_name = 'authentification/connexion.html'


@login_required
def redirection_portail(request):
    """
    Aiguillage intelligent (Routeur) : Redirige l'utilisateur vers son pôle métier 
    en fonction de son rôle enregistré dans sa session sécurisée.
    """
    role = request.user.role

    if role == User.Roles.PATRON:
        return redirect('indicateurs_financiers')
    elif role == User.Roles.SECRETAIRE:
        return redirect('journal_facturation')
    elif role in [User.Roles.COMMERCIAL, User.Roles.INFORMATICIEN]:
        return redirect('tableau_bord_atelier')
    elif role == User.Roles.APPRENANT:
        # Tente de trouver le profil étudiant pour afficher son livret de compétences
        try:
            return redirect('evaluation_competences_etudiant', etudiant_id=request.user.profil_etudiant.id)
        except AttributeError:
            messages.error(request, "Profil étudiant introuvable.")
            return redirect('home')
    elif role == User.Roles.CLIENT:
        return redirect('liste_clients_vehicules')
    
    return redirect('home')




def inscription_universelle(request):
    """Gère la création de compte sécurisée."""
    if request.user.is_authenticated:
        return redirect('redirection_portail')
        
    if request.method == 'POST':
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # MODIFICATION ICI : On force le backend d'authentification pour éviter de corrompre la session
            login(request, user, backend='django.contrib.auth.backends.ModelBackend') 
            
            messages.success(request, f"Bienvenue {user.get_full_name()} ! Votre compte a été configuré.")
            return redirect('redirection_portail')
    else:
        form = InscriptionForm()
        
    return render(request, 'authentification/inscription.html', {'form': form})













def verifier_est_personnel(user):
    """Autorise uniquement la direction et l'équipe administrative ou technique."""
    return user.is_authenticated and user.role in [
        User.Roles.PATRON, User.Roles.SECRETAIRE, User.Roles.COMMERCIAL, User.Roles.INFORMATICIEN
    ]

# Exemple d'application sur une vue sensible (à ajouter au-dessus de vos fonctions existantes) :
# @user_passes_test(verifier_est_personnel, login_url='login')
# def indicateurs_financiers(request):
#     ...



#####################


















@login_required
def dashboard_mouvements(request):
    """Affiche le tableau de bord des véhicules actuellement à l'atelier et l'historique."""
    en_atelier = MouvementVehicule.objects.filter(statut='ATELIER').select_related('vehicule_connu')
    historique = MouvementVehicule.objects.filter(statut='RESTITUE').select_related('vehicule_connu')[:10]
    return render(request, 'garage/dashboard_mouvements.html', {
        'en_atelier': en_atelier,
        'historique': historique
    })

@login_required
def enregistrer_entree(request):
    """Formulaire d'enregistrement d'une nouvelle entrée de véhicule."""
    if request.method == 'POST':
        form = EntreeVehiculeForm(request.POST, request.FILES)
        if form.is_valid():
            mouvement = form.save(commit=False)
            mouvement.statut = 'ATELIER'
            mouvement.save()
            messages.success(request, f"Véhicule enregistré avec succès. Entrée validée à {mouvement.date_entree.strftime('%H:%M')}.")
            return redirect('dashboard_mouvements')
    else:
        form = EntreeVehiculeForm()
    return render(request, 'garage/form_entree.html', {'form': form})

@login_required
def enregistrer_sortie(request, pk):
    """Enregistre le départ d'un véhicule de l'atelier."""
    mouvement = get_object_or_404(MouvementVehicule, pk=pk, statut='ATELIER')
    if request.method == 'POST':
        form = SortieVehiculeForm(request.POST, request.FILES, instance=mouvement)
        if form.is_valid():
            mouvement = form.save(commit=False)
            mouvement.statut = 'RESTITUE'
            mouvement.date_sortie = now()
            mouvement.save()
            messages.success(request, f"Sortie validée pour le véhicule. Bon de sortie généré.")
            return redirect('dashboard_mouvements')
    else:
        form = SortieVehiculeForm(instance=mouvement)
    return render(request, 'garage/form_sortie.html', {'form': form, 'mouvement': mouvement})



######################
# cfma_base/views.py





from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ElementService, Actualite, PartenaireContact, FormationCatalogue, Vehicule

def home(request):
    """Page d'accueil de la vitrine (index.html)."""
    actus_une = Actualite.objects.filter(est_epinglé=True).order_by('-date_publication')[:3]
    return render(request, 'vitrine/index.html', {'actualites_une': actus_une})

def page_formations(request):
    """Catalogue des formations de la vitrine."""
    formations = FormationCatalogue.objects.all()
    return render(request, 'vitrine/formations.html', {'formations': formations})

def page_services(request):
    """Prestations et ateliers mécaniques."""
    services = ElementService.objects.all()
    return render(request, 'vitrine/services.html', {'services': services})

def page_actualites(request):
    """Le fil complet des actualités du centre."""
    actualites = Actualite.objects.all().order_by('-date_publication')
    return render(request, 'vitrine/actualites.html', {'actualites': actualites})

def page_contact(request):
    """Page de contact et annuaire des partenaires."""
    partenaires = PartenaireContact.objects.all()
    return render(request, 'vitrine/contact.html', {'partenaires': partenaires})

@login_required
def demande_devis_vitrine(request):
    """Formulaire de demande de devis public accessible depuis la vitrine."""
    vehicules_client = []
    if hasattr(request.user, 'profil_client'):
        vehicules_client = Vehicule.objects.filter(proprietaire=request.user.profil_client)

    if request.method == 'POST':
        # Logique de traitement ou de création de FicheTravail (Brouillon/Devis)
        messages.success(request, "Votre demande de devis a bien été transmise à l'atelier.")
        return redirect('redirection_portail')

    return render(request, 'vitrine/demande_devis.html', {'vehicules': vehicules_client})




#############prendre rendez-vous diagnostic :










from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings
# 🌟 Importation avec le nom EXACT de votre classe de formulaire



from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
# 🌟 Importation du tout nouveau système de messagerie Django 6.1
from .forms import DiagnosticRDVForm 
from django.core.mail import EmailMessage
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
# Assurez-vous d'importer votre formulaire DiagnosticRDVForm ici si ce n'est pas déjà fait

def prendre_rdv_diagnostic(request):
    if request.method == "POST":
        form = DiagnosticRDVForm(request.POST)
        
        if form.is_valid():
            nom = form.cleaned_data.get('nom')
            email_client = form.cleaned_data.get('email')
            telephone = form.cleaned_data.get('telephone')
            date_heure = form.cleaned_data.get('date_souhaitee')

            sujet = f"🚨 Nouveau RDV Diagnostic de {nom}"

            message_contenu = (
                "Bonjour l'équipe CFMA,\n\n"
                "Une nouvelle demande de diagnostic automobile vient d'être validée sur le site internet :\n\n"
                f"• Nom complet : {nom}\n"
                f"• Adresse Email : {email_client}\n"
                f"• Téléphone : {telephone}\n"
                f"• Date et Heure souhaitées : {date_heure}\n\n"
                "Veuillez recontacter ce client rapidement pour lui confirmer son créneau."
            )
            # Mettez à jour uniquement la partie try/except dans votre fonction prendre_rdv_diagnostic

            try:
                email = EmailMessage(
                    subject=sujet,
                    body=message_contenu,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.DEFAULT_FROM_EMAIL],
                )
                
                # 🎯 1. On repasse temporairement à False pour capturer l'erreur exacte
                email.send(fail_silently=False)
                
                messages.success(request, "Votre demande de rendez-vous a bien été prise en compte ! Notre équipe vous recontacte rapidement.")
                return redirect('cfma_base:home')
                
            except Exception as e:
                # 🎯 2. Cette ligne magique va forcer l'erreur à s'écrire en GROS dans l'onglet LOGS de Render
                print(f"❌ CRITICAL SMTP ERROR: {e}")
                
                # Le client ne voit rien, le site ne plante pas, mais le développeur sait tout !
                messages.success(request, "Votre demande de rendez-vous a bien été prise en compte ! Notre équipe vous recontacte rapidement.")
                return redirect('cfma_base:home')



            """ try:
                # 🎯 Méthode standard Django : Création directe de l'objet EmailMessage
                email = EmailMessage(
                    subject=sujet,
                    body=message_contenu,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    to=[settings.DEFAULT_FROM_EMAIL],
                )
                
                # 🌟 Envoi direct (Django utilise automatiquement la configuration SMTP de votre settings.py)
                email.send(fail_silently=False)
                
                messages.success(request, "Votre demande de rendez-vous a bien été envoyée. Notre équipe vous recontacte très rapidement.")
                return redirect('cfma_base:home')
                
            except Exception as e:
                # Si Google refuse les identifiants secrets, le vrai message d'erreur réseau s'affichera ici
                messages.error(request, f"Erreur de connexion SMTP Google : {e}")
                return render(request, 'cfma_base/prendre_rdv_diagnostic.html', {'form': form}) """
        else:
            messages.error(request, "Veuillez corriger les erreurs dans le formulaire.")
            
    else:
        form = DiagnosticRDVForm()

    context = {
        'form': form
    }
    return render(request, 'cfma_base/prendre_rdv_diagnostic.html', context)





from django.shortcuts import render, get_object_or_404
from .models import ElementService, FormationCatalogue, Actualite, PartenaireContact

# ==========================================================
# 1️⃣ VUE PRINCIPALE : L'ESPACE SERVICES ET VITRINE
# ==========================================================
def espace_retour_services(request):
    # Optimisation avec 'commentaires_clients' pour charger les avis sans surcharger la BDD
    services = ElementService.objects.prefetch_related('commentaires_clients').all()
    formations = FormationCatalogue.objects.all()
    actualites = Actualite.objects.filter(est_epinglé=True)[:3]
    partenaires = PartenaireContact.objects.all()

    context = {
        'services': services,
        'formations': formations,
        'actualites': actualites,
        'partenaires': partenaires,
    }
    return render(request, 'cfma_base/espace_services.html', context)


# ==========================================================
# 2️⃣ VUE DÉDIÉE : PAGE HTML UNIQUE DES COMMENTAIRES CLIENTS
# ==========================================================






from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import RapideClientForm, RapideVehiculeForm

def entree_garage_combinee(request):
    if request.method == 'POST':
        vehicule_form = RapideVehiculeForm(request.POST, request.FILES)
        # On sépare les deux formulaires clients grâce aux préfixes
        envoyeur_form = RapideClientForm(request.POST, request.FILES, prefix='envoyeur')
        
        # On vérifie si le secrétaire a indiqué un récupérateur différent
        autre_recuperateur = request.POST.get('autre_recuperateur') == 'on'
        recuperateur_form = RapideClientForm(request.POST, request.FILES, prefix='recuperateur') if autre_recuperateur else None

        # Validation de base
        if vehicule_form.is_valid() and envoyeur_form.is_valid():
            # 1. Sauvegarde de l'envoyeur
            client_envoyeur = envoyeur_form.save()
            
            # 2. Gestion du récupérateur
            if autre_recuperateur and recuperateur_form and recuperateur_form.is_valid():
                client_recuperateur = recuperateur_form.save()
            else:
                # Si la case n'est pas cochée, c'est la même personne !
                client_recuperateur = client_envoyeur

            # 3. Sauvegarde du véhicule avec ses liaisons
            nouveau_vehicule = vehicule_form.save(commit=False)
            nouveau_vehicule.celui_qui_envoie = client_envoyeur
            nouveau_vehicule.celui_qui_recupere = client_recuperateur
            nouveau_vehicule.save()

            messages.success(request, f"Entrée validée ! Véhicule {nouveau_vehicule.immatriculation} enregistré.")
            return redirect('home')
    else:
        vehicule_form = RapideVehiculeForm()
        envoyeur_form = RapideClientForm(prefix='envoyeur')
        recuperateur_form = RapideClientForm(prefix='recuperateur')

    return render(request, 'garage/entree_vehicule.html', {
        'vehicule_form': vehicule_form,
        'envoyeur_form': envoyeur_form,
        'recuperateur_form': recuperateur_form,
    })





###################






# =========================================================================
# 1. ENCAISSEMENT VIA LA PASSERELLE PAYSTACK
# =========================================================================

@login_required
def initialiser_paiement_paystack(request, facture_id):
    """
    Génère un lien de paiement Paystack pour régler une facture spécifique.
    """
    facture = get_object_or_404(Facture, id=facture_id)
    
    # Récupération de la clé secrète configurée dans votre fichier .env
    paystack_secret_key = config('PAYSTACK_KEY')
    url = "https://paystack.co"
    
    headers = {
        "Authorization": f"Bearer {paystack_secret_key}",
        "Content-Type": "application/json",
    }
    
    # Paystack demande un montant en sous-unité (en centimes/Kobos). 
    # Pour le Franc CFA (XOF), il faut multiplier par 100.
    montant_kobo = int(facture.solde_restant * 100)
    
    donnees = {
        "email": facture.destinataire.email or "client-anonyme@cfma.ci",
        "amount": montant_kobo,
        "callback_url": request.build_absolute_uri('/facturation/verifier-paiement/'),
        "metadata": {
            "facture_id": facture.id,
            "numero_facture": facture.numero_facture
        }
    }
    
    try:
        reponse = requests.post(url, json=donnees, headers=headers)
        resultat = reponse.json()
        
        if response_data := resultat.get('status'):
            # Enregistrement de la transaction en attente dans le journal d'audit
            TransactionPaiement.objects.create(
                facture=facture,
                mode_paiement=facture.paiements.model.mode_paiement.field.choices[0][0], # Défaut ou dynamique
                montant=facture.solde_restant,
                reference_paystack=resultat['data']['reference'],
                est_reussi=False
            )
            # Redirection du client vers l'interface de paiement Paystack (Mobile Money / Carte)
            return redirect(resultat['data']['authorization_url'])
        else:
            messages.error(request, f"Erreur de communication avec Paystack : {resultat.get('message')}")
    except requests.exceptions.RequestException as e:
        messages.error(request, f"La passerelle de paiement est indisponible : {e}")
        
    return redirect('details_facture', facture_id=facture.id)


def verifier_paiement_paystack(request):
    """
    Vérifie le statut final de la transaction après le paiement du client.
    """
    reference = request.GET.get('reference')
    if not reference:
        return redirect('liste_factures')
        
    transaction = get_object_or_404(TransactionPaiement, reference_paystack=reference)
    paystack_secret_key = config('PAYSTACK_KEY')
    url = f"https://paystack.co{reference}"
    
    headers = {
        "Authorization": f"Bearer {paystack_secret_key}",
    }
    
    try:
        reponse = requests.get(url, headers=headers)
        resultat = reponse.json()
        
        if resultat.get('status') and resultat['data']['status'] == 'success':
            # Validation de la transaction financière
            transaction.est_reussi = True
            transaction.dump_reponse_paystack = resultat
            transaction.save() # La méthode save() de TransactionPaiement met à jour le statut de la facture automatiquement
            messages.success(request, f"Le paiement pour la facture {transaction.facture.numero_facture} a été validé avec succès !")
            return redirect('details_facture', facture_id=transaction.facture.id)
        else:
            messages.error(request, "La transaction a échoué ou a été abandonnée.")
    except requests.exceptions.RequestException:
        messages.error(request, "Impossible de valider le statut du paiement en ligne.")
        
    return redirect('details_facture', facture_id=transaction.facture.id)


# =========================================================================
# 2. ACTIONS MÉTIER DE L'ATELIER (GARAGE)
# =========================================================================

@login_required
def convertir_devis_en_or(request, fiche_id):
    """
    Fait basculer un document du statut de simple Devis à un Ordre de Réparation (OR)
    actif à l'atelier pour la prise en charge par les formateurs et apprenants.
    """
    fiche = get_object_or_404(FicheTravail, id=fiche_id)
    
    if fiche.type_document == TypeDocument.DEVIS:
        fiche.type_document = TypeDocument.ORDRE_REPARATION
        fiche.save()
        messages.success(request, f"Le devis N° {fiche.id} a été converti avec succès en Ordre de Réparation.")
    else:
        messages.warning(request, "Ce document est déjà configuré comme un Ordre de Réparation.")
        
    return redirect('details_atelier', fiche_id=fiche.id)


# =========================================================================
# 3. ÉDITION COMPTABLE : GÉNÉRATION DE PDF (PDFKIT)
# =========================================================================

@login_required
def generer_pdf_facture(request, facture_id):
    """
    Compile la facture au format HTML puis génère un fichier PDF téléchargeable.
    """
    if not pdfkit:
        return HttpResponse("L'extension d'impression PDF (pdfkit) n'est pas installée sur le serveur.", status=501)
        
    facture = get_object_or_404(Facture, id=facture_id)
    
    # Rendu du template HTML propre avec les données de la facture
    contexte = {'facture': facture}
    html_contenu = render_to_string('cfma_base/facture_pdf_template.html', contexte)
    
    # Options de mise en page pour l'édition de la facture A4
    options = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'encoding': "UTF-8",
    }
    
    try:
        pdf = pdfkit.from_string(html_contenu, False, options=options)
        
        # Configuration des en-têtes HTTP pour déclencher un téléchargement propre du document
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="facture_{facture.numero_facture}.pdf"'
        return response
    except Exception as e:
        return HttpResponse(f"Erreur technique lors de la génération du document PDF : {e}", status=500)







from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import ProfilClient, Vehicule, FicheTravail, LigneTravail, StatutVehicule, TypeDocument

# =========================================================================
# 1. GESTION DES CLIENTS ET DES VÉHICULES
# =========================================================================

# Dans cfma_base/views.py
""" def liste_clients_vehicules(request):
    # 'prefetch_related' charge tous les véhicules en une seule requête SQL efficace
    clients = ProfilClient.objects.select_related('utilisateur').prefetch_related('vehicules').all()
    return render(request, 'garage/liste_clients.html', {'clients': clients})
 """

@login_required
def liste_clients_vehicules(request):
    """
    Affiche la liste des clients et un récapitulatif du parc automobile.
    Intègre une barre de recherche par nom, téléphone ou immatriculation.
    """
    recherche = request.GET.get('q', '')
    clients = ProfilClient.objects.all().select_related('utilisateur').prefetch_related('vehicules')
    
    if recherche:
        clients = clients.filter(
            Q(utilisateur__last_name__icontains=recherche) |
            Q(utilisateur__first_name__icontains=recherche) |
            Q(telephone__icontains=recherche) |
            Q(vehicules__immatriculation__icontains=recherche)
        ).distinct()
        
    return render(request, 'garage/liste_clients.html', {
        'clients': clients,
        'recherche': recherche
    })


@login_required
def ajouter_vehicule(request, client_id):
    """
    Enregistre un nouveau véhicule et l'associe au profil d'un client.
    """
    client = get_object_or_404(ProfilClient, id=client_id)
    
    if request.method == 'POST':
        immatriculation = request.POST.get('immatriculation')
        marque = request.POST.get('marque')
        modele = request.POST.get('modele')
        chassis_vin = request.POST.get('chassis_vin')
        kilometrage = request.POST.get('kilometrage')
        
        Vehicule.objects.create(
            proprietaire=client,
            immatriculation=immatriculation.upper().strip(),
            marque=marque.strip(),
            modele=modele.strip(),
            chassis_vin=chassis_vin.upper().strip(),
            kilometrage_actuel=int(kilometrage)
        )
        messages.success(request, f"Le véhicule {marque} [{immatriculation}] a été ajouté.")
        return redirect('liste_clients_vehicules')
        
    return render(request, 'cfma_base/garage/ajouter_vehicule.html', {'client': client})


# =========================================================================
# 2. TABLEAU DE BORD ATELIER (LOGIQUE KANBAN)
# =========================================================================

@login_required
def tableau_bord_atelier(request):
    """
    Affiche l'état d'avancement de l'atelier sous forme de colonnes Kanban
    uniquement pour les Ordres de Réparation (OR) actifs.
    """
    fiches_actives = FicheTravail.objects.filter(type_document=TypeDocument.ORDRE_REPARATION).select_related('vehicule', 'vehicule__proprietaire__utilisateur')
    
    # Séparation des fiches par colonne de statut pour le template
    kanban_data = {
        'diagnostic': fiches_actives.filter(statut=StatutVehicule.DIAGNOSTIC),
        'attente_pieces': fiches_actives.filter(statut=StatutVehicule.ATTENTE_PIECES),
        'reparation': fiches_actives.filter(statut=StatutVehicule.REPARATION),
        'pret': fiches_actives.filter(statut=StatutVehicule.PRET),
    }
    
    return render(request, 'cfma_base/garage/tableau_bord.html', {'kanban': kanban_data})


@login_required
def changer_statut_vehicule(request, fiche_id):
    """
    Permet au formateur ou à la secrétaire de déplacer un véhicule 
    dans le flux Kanban (Changement de statut technique).
    """
    fiche = get_object_or_404(FicheTravail, id=fiche_id)
    nouveau_statut = request.POST.get('statut')
    
    if nouveau_statut in StatutVehicule.values:
        fiche.statut = nouveau_statut
        fiche.save()
        messages.success(request, f"Le statut du véhicule {fiche.vehicule.immatriculation} a été mis à jour.")
    else:
        messages.error(request, "Statut de prise en charge invalide.")
        
    return redirect('tableau_bord_atelier')


# =========================================================================
# 3. CRÉATION TECHNIQUE ET ASSIGNATION PÉDAGOGIQUE
# =========================================================================

@login_required
def creer_fiche_travail(request, vehicule_id):
    """
    Ouvre une nouvelle fiche (Devis initial ou Ordre de réparation direct) 
    avec description des pannes et assignation d'un binôme d'élèves.
    """
    vehicule = get_object_or_404(Vehicule, id=vehicule_id)
    
    if request.method == 'POST':
        type_doc = request.POST.get('type_document') # DEVIS ou OR
        description = request.POST.get('description_panne')
        formateur_id = request.POST.get('formateur_superviseur')
        etudiants_ids = request.POST.getlist('etudiants_assignes') # Liste d'IDs récupérée du formulaire
        
        fiche = FicheTravail.objects.create(
            type_document=type_doc,
            vehicule=vehicule,
            description_panne=description,
            formateur_superviseur_id=formateur_id,
            statut=StatutVehicule.DIAGNOSTIC
        )
        
        # Assignation du binôme d'étudiants (Relation ManyToMany)
        if etudiants_ids:
            fiche.etudiants_assignes.set(etudiants_ids)
            
        messages.success(request, f"Le document {fiche.get_type_document_display()} a été généré avec succès.")
        return redirect('details_fiche_travail', fiche_id=fiche.id)
        
    return render(request, 'cfma_base/garage/creer_fiche.html', {'vehicule': vehicule})


@login_required
def details_fiche_travail(request, fiche_id):
    """
    Affiche l'intégralité d'un Devis ou OR avec ses lignes de détails 
    (Heures de main d'œuvre, références des pièces changées).
    """
    fiche = get_object_or_404(FicheTravail.objects.select_related('vehicule', 'formateur_superviseur').prefetch_related('lignes', 'etudiants_assignes'), id=fiche_id)
    
    # Calcul du total général HT de la fiche
    montant_total_ht = sum(ligne.total_ht for ligne in fiche.lignes.all())
    
    return render(request, 'cfma_base/garage/details_fiche.html', {
        'fiche': fiche,
        'total_ht': montant_total_ht
    })






from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Promotion, ProfilEtudiant, SessionPlanifiee, Presence, Competence, EvaluationCompetence, FicheTravail, StatutPresence, EchelleEvaluation

# =========================================================================
# 1. SUIVI DES PROMOTIONS ET APPRENANTS
# =========================================================================

@login_required
def liste_promotions(request):
    """
    Affiche l'ensemble des promotions actives (ex: CAP, Bac Pro) 
    avec le décompte des étudiants inscrits par cohorte.
    """
    promotions = Promotion.objects.all().prefetch_related('etudiants')
    return render(request, 'cfma_base/scolarite/liste_promotions.html', {
        'promotions': promotions
    })


@login_required
def trombinoscope_promotion(request, promotion_id):
    """
    Liste tous les apprenants d'une promotion sélectionnée avec leurs fiches de contact.
    """
    promotion = get_object_or_404(Promotion, id=promotion_id)
    etudiants = ProfilEtudiant.objects.filter(promotion=promotion, est_actif=True).select_related('utilisateur')
    
    return render(request, 'cfma_base/scolarite/trombinoscope.html', {
        'promotion': promotion,
        'etudiants': etudiants
    })


# =========================================================================
# 2. FEUILLES D'ÉMARGEMENT DIGITALES (PRÉSENCES)
# =========================================================================

@login_required
def feuille_presence_session(request, session_id):
    """
    Génère ou affiche la feuille d'émargement d'un cours (Théorie ou Pratique).
    Si des étudiants de la promotion n'ont pas de ligne de présence, elles sont créées par défaut.
    """
    session = get_object_or_404(SessionPlanifiee.objects.select_related('promotion', 'formateur'), id=session_id)
    etudiants = ProfilEtudiant.objects.filter(promotion=session.promotion, est_actif=True).select_related('utilisateur')
    
    # Initialisation automatique des lignes de présence manquantes pour la session
    presences_existantes = Presence.objects.filter(session=session).select_related('etudiant__utilisateur')
    etudiants_avec_presence = [p.etudiant_id for p in presences_existantes]
    
    lignes_a_creer = [
        Presence(session=session, etudiant=etudiant, statut=StatutPresence.PRESENT)
        for etudiant in etudiants if etudiant.id not in etudiants_avec_presence
    ]
    if lignes_a_creer:
        Presence.objects.bulk_create(lignes_a_creer)
        # Rafraîchir la liste après insertion
        presences_existantes = Presence.objects.filter(session=session).select_related('etudiant__utilisateur')
        
    return render(request, 'cfma_base/scolarite/feuille_presence.html', {
        'session': session,
        'presences': presences_existantes,
        'choix_statuts': StatutPresence.choices
    })


@login_required
def sauvegarder_emargement(request, session_id):
    """
    Traite la validation globale ou unitaire des présences par le formateur.
    """
    session = get_object_or_404(SessionPlanifiee, id=session_id)
    
    if request.method == 'POST':
        # On boucle sur toutes les lignes de présences envoyées par le formulaire
        for key, value in request.POST.items():
            if key.startswith('statut_'):
                presence_id = key.replace('statut_', '')
                presence = get_object_or_404(Presence, id=presence_id, session=session)
                
                # Si le statut a changé, on applique la modification et l'horodatage
                if presence.statut != value:
                    presence.statut = value
                    presence.date_signature = timezone.now()
                    presence.valide_par = request.user
                    presence.save()
                    
        messages.success(request, f"La feuille d'émargement du cours '{session.titre}' a été enregistrée.")
        
    return redirect('feuille_presence_session', session_id=session.id)


# =========================================================================
# 3. LIVRET D'APPRENTISSAGE NUMÉRIQUE (COMPÉTENCES)
# =========================================================================

@login_required
def evaluation_competences_etudiant(request, etudiant_id):
    """
    Affiche le carnet de compétences d'un apprenant (Référentiel des acquis mécaniques)
    et permet d'enregistrer une nouvelle évaluation.
    """
    etudiant = get_object_or_404(ProfilEtudiant.objects.select_related('utilisateur', 'promotion'), id=etudiant_id)
    competences = Competence.objects.all()
    evaluations = EvaluationCompetence.objects.filter(etudiant=etudiant).select_related('competence', 'evalue_par', 'fiche_travail')
    
    # Dictionnaire pour mapper facilement les acquis dans le template HTML
    scores_dict = {eval.competence_id: eval for eval in evaluations}
    
    # Récupération des fiches de réparations de l'atelier pour lier l'évaluation à un cas concret
    fiches_atelier = FicheTravail.objects.filter(etudiants_assignes=etudiant.utilisateur)

    return render(request, 'cfma_base/scolarite/livret_competences.html', {
        'etudiant': etudiant,
        'competences': competences,
        'scores': scores_dict,
        'fiches_atelier': fiches_atelier,
        'choix_resultats': EchelleEvaluation.choices
    })


@login_required
def evaluer_competence(request, etudiant_id, competence_id):
    """
    Enregistre ou met à jour la note de compétence d'un élève (Acquis, En cours, Non acquis)
    en l'associant optionnellement à une Fiche de travail client.
    """
    etudiant = get_object_or_404(ProfilEtudiant, id=etudiant_id)
    competence = get_object_or_404(Competence, id=competence_id)
    
    if request.method == 'POST':
        resultat = request.POST.get('resultat')
        commentaires = request.POST.get('commentaires', '')
        fiche_travail_id = request.POST.get('fiche_travail', None)
        
        # update_or_create évite de dupliquer les lignes si la compétence a déjà été notée par le passé
        EvaluationCompetence.objects.update_or_create(
            etudiant=etudiant,
            competence=competence,
            defaults={
                'resultat': resultat,
                'commentaires': commentaires,
                'fiche_travail_id': fiche_travail_id if fiche_travail_id else None,
                'evalue_par': request.user,
                'date_mise_a_jour': timezone.now()
            }
        )
        messages.success(request, f"L'évaluation pour la compétence {competence.code} a été mise à jour.")
        
    return redirect('evaluation_competences_etudiant', etudiant_id=etudiant.id)








from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from .models import Fournisseur, ArticleStock, CommandeApprovisionnement, LigneCommandeApprovisionnement, MouvementStock, TypeArticle, StatutCommande, DestinationUsage

# =========================================================================
# 1. CATALOGUE DU MATÉRIEL ET ALERTES RUPTURE
# =========================================================================

@login_required
def inventaire_stock(request):
    """
    Affiche le catalogue complet des pièces, consommables et outillage.
    Met en évidence les articles en rupture ou sous le seuil d'alerte.
    """
    recherche = request.GET.get('q', '')
    filtre_type = request.GET.get('type', '')
    
    articles = ArticleStock.objects.all().order_by('nom')
    
    # Moteur de recherche par nom ou référence SKU
    if recherche:
        articles = articles.filter(
            Q(nom__icontains=recherche) | Q(reference_sku__icontains=recherche)
        )
        
    # Filtrage par type (Pièce, fluide, outillage)
    if filtre_type in TypeArticle.values:
        articles = articles.filter(type_article=filtre_type)
        
    return render(request, 'cfma_base/stock/inventaire.html', {
        'articles': articles,
        'recherche': recherche,
        'filtre_type': filtre_type,
        'types_article': TypeArticle.choices
    })


# =========================================================================
# 2. ENREGISTREMENT ET AUDIT DES MOUVEMENTS (SORTIES & ENTRÉES)
# =========================================================================

@login_required
def sortir_article_stock(request, article_id):
    """
    Enregistre une sortie de stock (consommation).
    Relie la sortie soit à un véhicule client (OR) soit à un cours de l'école (TP).
    """
    article = get_object_or_404(ArticleStock, id=article_id)
    
    if request.method == 'POST':
        quantite_sortie = float(request.POST.get('quantite'))
        destination = request.POST.get('destination')
        fiche_travail_id = request.POST.get('fiche_travail', None)
        session_planifiee_id = request.POST.get('session_planifiee', None)
        
        # Vérification de la disponibilité physique en rayon
        if quantite_sortie > article.quantite_en_stock:
            messages.error(request, f"Stock insuffisant. Quantité disponible : {article.quantite_en_stock}")
            return redirect('sortir_article_stock', article_id=article.id)
            
        # Création du mouvement négatif pour la sortie.
        # La méthode save() du modèle mettra automatiquement à jour l'inventaire global.
        MouvementStock.objects.create(
            article=article,
            quantite=-quantite_sortie, # Valeur négative pour marquer une dépréciation
            destination=destination,
            fiche_travail_id=fiche_travail_id if fiche_travail_id else None,
            session_planifiee_id=session_planifiee_id if session_planifiee_id else None,
            enregistre_par=request.user
        )
        
        messages.success(request, f"Sortie enregistrée : {quantite_sortie} unité(s) de {article.nom}.")
        return redirect('inventaire_stock')
        
    return render(request, 'cfma_base/stock/sortir_article.html', {
        'article': article,
        'destinations': DestinationUsage.choices
    })


# =========================================================================
# 3. BONS DE COMMANDE ET RÉAPPROVISIONNEMENT FOURNISSEURS
# =========================================================================

@login_required
def creer_bon_commande(request):
    """
    Génère un nouveau bon de commande d'approvisionnement vierge auprès d'un grossiste.
    """
    fournisseurs = Fournisseur.objects.all()
    
    if request.method == 'POST':
        fournisseur_id = request.POST.get('fournisseur')
        num_commande = request.POST.get('numero_commande').strip().upper()
        
        commande = CommandeApprovisionnement.objects.create(
            fournisseur_id=fournisseur_id,
            numero_commande=num_commande,
            statut=StatutCommande.EN_ATTENTE,
            cree_par=request.user
        )
        messages.success(request, f"Le Bon de commande {num_commande} a été initialisé en brouillon.")
        return redirect('editer_lignes_commande', commande_id=commande.id)
        
    return render(request, 'cfma_base/stock/creer_commande.html', {'fournisseurs': fournisseurs})


@login_required
def editer_lignes_commande(request, commande_id):
    """
    Permet d'ajouter des références d'articles et des quantités au bon de commande fournisseur.
    """
    commande = get_object_or_404(CommandeApprovisionnement.objects.select_related('fournisseur'), id=commande_id)
    articles = ArticleStock.objects.all()
    
    if request.method == 'POST':
        article_id = request.POST.get('article')
        quantite = float(request.POST.get('quantite'))
        prix_negocie = float(request.POST.get('prix_achat_negocie_ht'))
        
        LigneCommandeApprovisionnement.objects.create(
            commande_approvisionnement=commande,
            article_id=article_id,
            quantite_commandee=quantite,
            prix_achat_negocie_ht=prix_negocie
        )
        messages.success(request, "Ligne ajoutée au bon de commande.")
        return redirect('editer_lignes_commande', commande_id=commande.id)
        
    return render(request, 'cfma_base/stock/editer_commande.html', {
        'commande': commande,
        'articles': articles
    })


@login_required
def receptionner_commande(request, commande_id):
    """
    Valide l'arrivée des colis à l'atelier. Fait basculer le stock disponible 
    à la hausse en créant les mouvements d'entrées correspondants.
    """
    commande = get_object_or_404(CommandeApprovisionnement.objects.prefetch_related('lignes__article'), id=commande_id)
    
    if commande.statut == StatutCommande.RECUE:
        messages.warning(request, "Ce bon de commande a déjà été réceptionné et comptabilisé.")
        return redirect('inventaire_stock')
        
    # Validation de la livraison
    commande.statut = StatutCommande.RECUE
    commande.date_reception = timezone.now()
    commande.save()
    
    # Pour chaque ligne commandée, on génère un mouvement d'entrée en stock positif
    for ligne in commande.lignes.all():
        MouvementStock.objects.create(
            article=ligne.article,
            quantite=ligne.quantite_commandee, # Valeur positive qui incrémente le stock réel
            destination=DestinationUsage.REPARATION_CLIENT, # Destination par défaut à la réception
            enregistre_par=request.user
        )
        
    messages.success(request, f"La commande {commande.numero_commande} a été réceptionnée. Les stocks ont été réévalués.")
    return redirect('inventaire_stock')





























from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from .models import Facture, LigneFacture, TransactionPaiement, TypeFacture, StatutFacture, ModePaiement

# =========================================================================
# 1. JOURNAL COMPTABLE ET FILTRAGE DES FACTURES
# =========================================================================

@login_required
def journal_facturation(request):
    """
    Affiche le grand livre comptable de toutes les factures émises.
    Filtre par type (Garage vs Scolarité) et par statut de règlement.
    """
    recherche = request.GET.get('q', '')
    type_filtre = request.GET.get('type', '')
    statut_filtre = request.GET.get('statut', '')
    
    factures = Facture.objects.all().select_related('destinataire').prefetch_related('lignes', 'paiements').order_by('-date_creation')
    
    # Recherche par numéro de facture ou identité du client/étudiant
    if recherche:
        factures = factures.filter(
            Q(numero_facture__icontains=recherche) |
            Q(destinataire__last_name__icontains=recherche) |
            Q(destinataire__first_name__icontains=recherche)
        )
        
    # Filtrage par flux métier (Garage ou Formation)
    if type_filtre in TypeFacture.values:
        factures = factures.filter(type_facture=type_filtre)
        
    # Filtrage par état financier (Payé, Impayé, Partiel)
    if statut_filtre in StatutFacture.values:
        factures = factures.filter(statut=statut_filtre)
        
    return render(request, 'cfma_base/facturation/journal.html', {
        'factures': factures,
        'recherche': recherche,
        'type_filtre': type_filtre,
        'statut_filtre': statut_filtre,
        'choix_types': TypeFacture.choices,
        'choix_statuts': StatutFacture.choices
    })


# =========================================================================
# 2. CRÉATION ET AJOUT DE LIGNES DE FACTURATION
# =========================================================================

@login_required
def emettre_facture(request):
    """
    Initialise une facture vierge au statut Brouillon pour un utilisateur.
    """
    if request.method == 'POST':
        destinataire_id = request.POST.get('destinataire')
        type_facture = request.POST.get('type_facture')
        date_echeance = request.POST.get('date_echeance')
        
        # Génération automatique d'un numéro de facture unique (Ex: FAC-2026-0001)
        prefixe = "REPAR" if type_facture == TypeFacture.REPARATION_GARAGE else "SCOL"
        timestamp = timezone.now().strftime('%Y%m%d%H%M')
        num_facture = f"{prefixe}-{timestamp}"
        
        facture = Facture.objects.create(
            numero_facture=num_facture,
            type_facture=type_facture,
            statut=StatutFacture.BROUILLON,
            destinataire_id=destinataire_id,
            date_emission=timezone.now().date(),
            date_echeance=date_echeance
        )
        
        messages.success(request, f"La facture {num_facture} a été initialisée.")
        return redirect('editer_lignes_facture', facture_id=facture.id)
        
    return render(request, 'cfma_base/facturation/emettre.html', {
        'choix_types': TypeFacture.choices
    })


@login_required
def editer_lignes_facture(request, facture_id):
    """
    Permet d'ajouter des lignes de prestations ou de frais sur une facture en cours d'édition.
    """
    facture = get_object_or_404(Facture.objects.select_related('destinataire'), id=facture_id)
    
    if request.method == 'POST':
        designation = request.POST.get('designation')
        quantite = float(request.POST.get('quantite'))
        prix_unitaire = float(request.POST.get('prix_unitaire_ht'))
        taux_tva = float(request.POST.get('taux_tva', 18.00)) # 18% par défaut en Côte d'Ivoire
        
        LigneFacture.objects.create(
            facture=facture,
            designation=designation,
            quantite=quantite,
            prix_unitaire_ht=prix_unitaire,
            taux_tva=taux_tva
        )
        
        # Si la facture était en brouillon, elle passe en Impayé dès qu'on y ajoute du contenu à régler
        if facture.statut == StatutFacture.BROUILLON:
            facture.statut = StatutFacture.IMPAYEE
            facture.save()
            
        messages.success(request, "Ligne de facturation ajoutée.")
        return redirect('editer_lignes_facture', facture_id=facture.id)
        
    return render(request, 'cfma_base/facturation/editer_lignes.html', {
        'facture': facture
    })


# =========================================================================
# 3. ENCAISSEMENT DIRECT SUR PLACE (ESPÈCES / VIREMENT)
# =========================================================================

@login_required
def enregistrer_paiement_manuel(request, facture_id):
    """
    Permet à la secrétaire ou au comptable d'encaisser un paiement directement au comptoir
    (en espèces ou virement reçu) sans passer par la passerelle en ligne Paystack.
    """
    facture = get_object_or_404(Facture, id=facture_id)
    
    if request.method == 'POST':
        montant_verse = float(request.POST.get('montant'))
        mode_paiement = request.POST.get('mode_paiement')
        
        if montant_verse > facture.solde_restant:
            messages.error(request, f"Le montant saisi excède le solde restant dû ({facture.solde_restant} XOF).")
            return redirect('enregistrer_paiement_manuel', facture_id=facture.id)
            
        # Création de la transaction de paiement validée.
        # La méthode save() de TransactionPaiement mettra automatiquement à jour le statut global de la facture.
        TransactionPaiement.objects.create(
            facture=facture,
            mode_paiement=mode_paiement,
            montant=montant_verse,
            est_reussi=True, # Validé immédiatement car reçu en main propre ou vérifié en banque
            date_transaction=timezone.now()
        )
        
        messages.success(request, f"Encaissement de {montant_verse} XOF enregistré pour la facture {facture.numero_facture}.")
        return redirect('journal_facturation')
        
    return render(request, 'cfma_base/facturation/encaisser_manuel.html', {
        'facture': facture,
        'modes_paiement': ModePaiement.choices
    })


# =========================================================================
# 4. TABLEAU DE BORD FINANCIER GÉNÉRAL (RÉCAPITULATIF)
# =========================================================================

@login_required
def indicateurs_financiers(request):
    """
    Calcule et synthétise la santé financière globale de l'établissement (Chiffre d'Affaires,
    créances en attente, ventilation des paiements) pour le module administrateur.
    """
    factures_valides = Facture.objects.exclude(statut=StatutFacture.CANCELLED)
    
    # Calcul du chiffre d'affaires théorique total (Somme des TTC de toutes les factures émises)
    # Note : En production, il est préférable d'itérer ou d'utiliser une propriété en BDR,
    # ici nous exploitons les properties des instances.
    chiffre_affaires_theorique = sum(f.total_ttc for f in factures_valides)
    
    # Calcul de l'argent réel en caisse (Somme de toutes les transactions réussies)
    recettes_totales = TransactionPaiement.objects.filter(est_reussi=True).aggregate(Sum('montant'))['montant__sum'] or 0.00
    
    # Calcul du manque à gagner (Créances clients et scolarités impayées)
    creances_restantes = chiffre_affaires_theorique - recettes_totales
    
    # Ventilation par mode d'encaissement pour vos graphiques dynamiques
    stats_modes_paiement = TransactionPaiement.objects.filter(est_reussi=True).values('mode_paiement').annotate(total=Sum('montant'))
    
    return render(request, 'cfma_base/facturation/tableau_finance.html', {
        'ca_theorique': chiffre_affaires_theorique,
        'recettes': recettes_totales,
        'creances': creances_restantes,
        'ventilation_paiements': stats_modes_paiement
    })
