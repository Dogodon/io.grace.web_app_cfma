from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser
from django.db import models

#1
from django.contrib.auth.models import User

#2
from django.db import models
from django.contrib.auth.models import User

#3
from django.db import models
from django.contrib.auth.models import User

#4
from django.db import models
from django.contrib.auth.models import User

from django.conf import settings

from django.db.models import Sum

# Remplacer partout les relations :
# models.ForeignKey(User, ...) par models.ForeignKey(settings.AUTH_USER_MODEL, ...)

from django.db import connection




class User(AbstractUser):
    class Roles(models.TextChoices):
        PATRON = 'PATRON', 'Patron'
        SECRETAIRE = 'SECRETAIRE', 'Secrétaire'
        COMMERCIAL = 'COMMERCIAL', 'Commercial'
        CLIENT = 'CLIENT', 'Client'
        APPRENANT = 'APPRENANT', 'Apprenant'
        INFORMATICIEN = 'INFORMATICIEN', 'Informaticien'

    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.CLIENT)



###########################


class ElementService(models.Model):
    """Prestations proposées par le centre de diagnostic et l'atelier."""
    titre = models.CharField(max_length=150, verbose_name="Titre du service")
    icone_font_awesome = models.CharField(max_length=50, default="fa-car", verbose_name="Icône FontAwesome (ex: fa-wrench)")
    description = models.TextField(verbose_name="Description de la prestation")
    prix_public_indicatif = models.CharField(max_length=100, blank=True, null=True, verbose_name="Tarif indicatif")
    # 🎯 Champ image optionnel ajouté
    image = models.ImageField(upload_to="services/", blank=True, null=True, verbose_name="Image d'illustration (Optionnel)")

    class Meta:
        verbose_name = "Service de l'Atelier"
        verbose_name_plural = "Services de l'Atelier"

    def __str__(self):
        return self.titre


class Actualite(models.Model):
    """Journal des événements, rentrées académiques ou astuces techniques."""
    titre = models.CharField(max_length=200, verbose_name="Titre de l'article")
    contenu = models.TextField(verbose_name="Contenu de l'actualité")
    date_publication = models.DateTimeField(auto_now_add=True, verbose_name="Date de publication")
    est_epinglé = models.BooleanField(default=False, verbose_name="Mettre à la une ?")
    # 🎯 Champ image optionnel ajouté
    image = models.ImageField(upload_to="actualites/", blank=True, null=True, verbose_name="Image de l'article (Optionnel)")

    class Meta:
        verbose_name = "Actualité"
        verbose_name_plural = "Actualités"

    def __str__(self):
        return self.titre


class PartenaireContact(models.Model):
    """Liste des entreprises partenaires (garages, flottes, distributeurs de pièces)."""
    nom_societe = models.CharField(max_length=150, verbose_name="Nom de l'entreprise")
    # 🎯 Transformation : URL optionnelle remplacée par un fichier image physique local
    logo = models.ImageField(upload_to="partenaires/", blank=True, null=True, verbose_name="Logo de l'entreprise (Optionnel)")
    telephone_pro = models.CharField(max_length=20, verbose_name="Téléphone professionnel")
    email_pro = models.EmailField(verbose_name="Email professionnel")
    site_web = models.URLField(blank=True, null=True, verbose_name="Site Internet (Optionnel)")

    class Meta:
        verbose_name = "Partenaire / Contact"
        verbose_name_plural = "Partenaires / Contacts"

    def __str__(self):
        return self.nom_societe


class FormationCatalogue(models.Model):
    """Parcours de formation gérés dynamiquement pour la vitrine."""
    titre = models.CharField(max_length=150, verbose_name="Intitulé du diplôme")
    duree = models.CharField(max_length=50, verbose_name="Durée du cursus (ex: 2 ans)")
    badge_niveau = models.CharField(max_length=50, verbose_name="Niveau (ex: CAP, BAC PRO, CQP)")
    description_generale = models.TextField(verbose_name="Description générale")
    competences_cles = models.TextField(verbose_name="Compétences clés (Séparées par des virgules)")
    # 🎯 Champ image optionnel ajouté
    image = models.ImageField(upload_to="formations/", blank=True, null=True, verbose_name="Image de couverture (Optionnel)")

    @property
    def liste_competences(self):
        """Découpe la chaîne textuelle pour générer une liste propre dans le template."""
        return [c.strip() for c in self.competences_cles.split(',') if c.strip()]

    class Meta:
        verbose_name = "Formation du Catalogue"
        verbose_name_plural = "Formations du Catalogue"

    def __str__(self):
        return f"{self.badge_niveau} - {self.titre}"
    







class GalerieCommentaireClient(models.Model):
    # 🌟 Remplacement de la clé étrangère par un champ de texte simple autonome
    titre_prestation = models.CharField(max_length=150, default="Diagnostic / Réparation", verbose_name="Nom de la prestation concernée")
    auteur = models.CharField(max_length=150, verbose_name="Nom du client")
    statut_vehicule = models.CharField(max_length=150, verbose_name="Statut / Véhicule (ex: Propriétaire SUV)")
    commentaire = models.TextField(verbose_name="Commentaire Client")
    
    # Carrousel de 1 à 5 images
    image1 = models.ImageField(upload_to="galerie_clients/", verbose_name="Image 1 (Obligatoire)")
    image2 = models.ImageField(upload_to="galerie_clients/", blank=True, null=True, verbose_name="Image 2 (Optionnelle)")
    image3 = models.ImageField(upload_to="galerie_clients/", blank=True, null=True, verbose_name="Image 3 (Optionnelle)")
    image4 = models.ImageField(upload_to="galerie_clients/", blank=True, null=True, verbose_name="Image 4 (Optionnelle)")
    image5 = models.ImageField(upload_to="galerie_clients/", blank=True, null=True, verbose_name="Image 5 (Optionnelle)")

    class Meta:
        verbose_name = "Galerie Commentaire Client"
        verbose_name_plural = "Galeries Commentaires Clients"

    def __str__(self):
        return f"Avis Client de {self.auteur} - {self.titre_prestation}"



class GalerieCommentaireEvenement(models.Model):
    # Liste de choix pour le statut de l'événement
    STATUT_CHOICES = [
        ('en_cours', 'En cours'),
        ('a_venir', 'À venir'),
        ('termine', 'Terminé'),
    ]

    titre_evenement = models.CharField(max_length=150, default="Événement Académie", verbose_name="Nom de l'événement concerné")
    acteurs = models.CharField(max_length=150, verbose_name="Nom de l'acteur / étudiant")
    statut_evenement = models.CharField(
        max_length=20, 
        choices=STATUT_CHOICES, 
        default='en_cours', 
        verbose_name="Statut de l'événement"
    )
    commentaire = models.TextField(verbose_name="Commentaire Événement")
    
    # Carrousel de 1 à 5 images
    image1 = models.ImageField(upload_to="galerie_evenements/", verbose_name="Image 1 (Obligatoire)")
    image2 = models.ImageField(upload_to="galerie_evenements/", blank=True, null=True, verbose_name="Image 2 (Optionnelle)")
    image3 = models.ImageField(upload_to="galerie_evenements/", blank=True, null=True, verbose_name="Image 3 (Optionnelle)")
    image4 = models.ImageField(upload_to="galerie_evenements/", blank=True, null=True, verbose_name="Image 4 (Optionnelle)")
    image5 = models.ImageField(upload_to="galerie_evenements/", blank=True, null=True, verbose_name="Image 5 (Optionnelle)")

    class Meta:
        verbose_name = "Galerie Commentaire Événement"
        verbose_name_plural = "Galeries Commentaires Événements"

    def __str__(self):
        return f"Avis Événement de {self.acteurs} - {self.titre_evenement}"




class GalerieCFMA(models.Model):
    # Informations institutionnelles (Utilisées sur la page À Propos)
    nom_patron = models.CharField(max_length=150, default="M. KOUADIO YVES", verbose_name="Nom du Directeur / Patron")
    biographie_patron = models.TextField(blank=True, null=True, verbose_name="Biographie du Directeur")
    biographie_cfma = models.TextField(blank=True, null=True, verbose_name="Histoire et Biographie de CFMA")
    
    # Informations optionnelles sur les témoignages
    auteur = models.CharField(max_length=150, blank=True, null=True, verbose_name="Auteur du commentaire")
    statut_vehicule = models.CharField(max_length=150, blank=True, null=True, verbose_name="Statut / Véhicule (ex: Propriétaire SUV)")
    commentaire = models.TextField(blank=True, null=True, verbose_name="Commentaire additionnel")
    
    # Carrousel de 1 à 5 images du Centre CFMA
    image1 = models.ImageField(upload_to="galerie_cfma/", verbose_name="Image 1 (Obligatoire)")
    image2 = models.ImageField(upload_to="galerie_cfma/", blank=True, null=True, verbose_name="Image 2 (Optionnelle)")
    image3 = models.ImageField(upload_to="galerie_cfma/", blank=True, null=True, verbose_name="Image 3 (Optionnelle)")
    image4 = models.ImageField(upload_to="galerie_cfma/", blank=True, null=True, verbose_name="Image 4 (Optionnelle)")
    image5 = models.ImageField(upload_to="galerie_cfma/", blank=True, null=True, verbose_name="Image 5 (Optionnelle)")

    class Meta:
        verbose_name = "Galerie CFMA"
        verbose_name_plural = "Galeries CFMA"

    def __str__(self):
        # Sécurité pour éviter le NameError si le champ nom_patron est vide
        return f"Présentation CFMA - Directeur : {self.nom_patron}"



















##########################################VOITURE
from django.db import models
from django.utils.timezone import now

# cfma_base/models.py
from django.db import models
from django.utils import timezone
from django.conf import settings # Pour lier à votre Custom User

class Vehicule(models.Model):
    proprietaire = models.ForeignKey('ProfilClient', on_delete=models.CASCADE, related_name='vehicules', verbose_name="Propriétaire")
    immatriculation = models.CharField(max_length=20, unique=True, verbose_name="Immatriculation")
    marque = models.CharField(max_length=50, verbose_name="Marque")
    modele = models.CharField(max_length=50, verbose_name="Modèle")
    chassis_vin = models.CharField(max_length=17, unique=True, verbose_name="Châssis / VIN")
    kilometrage_actuel = models.PositiveIntegerField(verbose_name="Kilométrage actuel")
    photo = models.ImageField(upload_to="vehicules_photos/", blank=True, null=True, verbose_name="Photo du véhicule (Optionnelle)")
    date_mise_a_jour = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")

    class Meta:
        verbose_name = "Véhicule"
        verbose_name_plural = "Véhicules"
        db_table = 'cfma_base_vehicule' # 🎯 Très important : indique à Django de réutiliser la table déjà créée sur Render

    def __str__(self):
        return f"{self.marque} {self.modele} - {self.immatriculation}"
""" 
class Vehicule(models.Model):
    proprietaire = models.ForeignKey('ProfilClient', on_delete=models.CASCADE, related_name='vehicules', verbose_name="Propriétaire")
    immatriculation = models.CharField(max_length=20, unique=True, verbose_name="Immatriculation")
    marque = models.CharField(max_length=50, verbose_name="Marque")
    modele = models.CharField(max_length=50, verbose_name="Modèle")
    chassis_vin = models.CharField(max_length=17, unique=True, verbose_name="Châssis / VIN")
    kilometrage_actuel = models.PositiveIntegerField(verbose_name="Kilométrage actuel")
    photo = models.ImageField(upload_to="vehicules_photos/", blank=True, null=True, verbose_name="Photo du véhicule (Optionnelle)")
    date_mise_a_jour = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")

    class Meta:
        verbose_name = "Véhicule"
        verbose_name_plural = "Véhicules"

    def __str__(self):
        return f"{self.marque} {self.modele} - {self.immatriculation}"
 """

class MouvementVehicule(models.Model):
    STATUT_CHOICES = [
        ('ATELIER', 'En cours de travaux / En atelier'),
        ('RESTITUE', 'Restitué au client / Sortie validée'),
    ]
    
    CARBURANT_CHOICES = [
        ('VIDE', 'Vide (Réserve)'),
        ('1/4', '1/4'),
        ('1/2', '1/2'),
        ('3/4', '3/4'),
        ('PLEIN', 'Plein complet'),
    ]

    # 1. SUIVI GÉNÉRAL DU FLUX
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='ATELIER', verbose_name="Statut du véhicule")
    
    # 2. INFOS DE CELUI QUI DÉPOSE LA VOITURE (ENTRÉE)
    depose_nom = models.CharField(max_length=100, verbose_name="Nom (Déposant)")
    depose_prenom = models.CharField(max_length=100, blank=True, null=True, verbose_name="Prénom (Déposant) - Fac")
    depose_travail = models.CharField(max_length=100, blank=True, null=True, verbose_name="Profession/Entreprise - Fac")
    depose_image = models.ImageField(upload_to="mouvements/deposants/", blank=True, null=True, verbose_name="Photo de la pièce/visage - Fac")
    date_entree = models.DateTimeField(default=now, verbose_name="Date et Heure d'entrée")

    # 3. INFOS DU VÉHICULE (À L'ENTRÉE)
    vehicule_connu = models.ForeignKey(Vehicule, on_delete=models.SET_NULL, blank=True, null=True, related_name='mouvements', verbose_name="Véhicule enregistré (Si connu)")
    immatriculation_manuelle = models.CharField(max_length=20, blank=True, null=True, verbose_name="Immatriculation - Fac")
    photo_plaque = models.ImageField(upload_to="mouvements/plaques/", verbose_name="Photo de la plaque d'immatriculation (Obligatoire)")
    photo_voiture = models.ImageField(upload_to="mouvements/voitures_entree/", blank=True, null=True, verbose_name="Photo globale du véhicule - Fac")
    
    kilometrage_entree = models.PositiveIntegerField(verbose_name="Kilométrage à l'entrée")
    niveau_carburant_entree = models.CharField(max_length=10, choices=CARBURANT_CHOICES, default='1/4', verbose_name="Carburant à l'entrée")
    observations_dommages = models.TextField(blank=True, null=True, verbose_name="Bosses, rayures ou pannes apparentes - Fac")

    # 4. INFOS DE CELUI QUI RETIRE LA VOITURE (SORTIE)
    retrait_nom = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nom (Récupérateur) - Fac")
    retrait_prenom = models.CharField(max_length=100, blank=True, null=True, verbose_name="Prénom (Récupérateur) - Fac")
    retrait_travail = models.CharField(max_length=100, blank=True, null=True, verbose_name="Profession/Entreprise (Récupérateur) - Fac")
    retrait_image = models.ImageField(upload_to="mouvements/recuperateurs/", blank=True, null=True, verbose_name="Photo pièce/visage (Récupérateur) - Fac")
    date_sortie = models.DateTimeField(blank=True, null=True, verbose_name="Date et Heure de sortie")
    kilometrage_sortie = models.PositiveIntegerField(blank=True, null=True, verbose_name="Kilométrage à la sortie - Fac")

    class Meta:
        verbose_name = "Mouvement de Véhicule"
        verbose_name_plural = "Gestion des Entrées / Sorties"
        ordering = ['-date_entree']

    def __str__(self):
        immat = self.vehicule_connu.immatriculation if self.vehicule_connu else self.immatriculation_manuelle or "Inconnue"
        return f"Flux {immat} - Déposé par {self.depose_nom} ({self.get_statut_display()})"








#################################




class RDVDiagnostic(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom complet")
    email = models.EmailField(verbose_name="Adresse Email")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    date_souhaitee = models.DateTimeField(verbose_name="Date et Heure du RDV")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Créé le")

    class Meta:
        verbose_name = "Rendez-vous Diagnostic"
        verbose_name_plural = "Rendez-vous Diagnostics"
        ordering = ['-date_souhaitee']

    def __str__(self):
        return f"RDV de {self.nom} - {self.date_souhaitee.strftime('%d/%m/%Y %H:%M')}"





# =========================================================================
# 1. LISTES DE CHOIX (ENUMS)
# =========================================================================

class StatutVehicule(models.TextChoices):
    DIAGNOSTIC = 'DIAG', 'En diagnostic'
    ATTENTE_PIECES = 'ATTENTE', 'En attente de pièces'
    REPARATION = 'REPAR', 'En réparation'
    PRET = 'PRET', 'Prêt / Terminé'

class TypeDocument(models.TextChoices):
    DEVIS = 'DEVIS', 'Devis'
    ORDRE_REPARATION = 'OR', 'Ordre de Réparation'

class StatutPresence(models.TextChoices):
    PRESENT = 'PRESENT', 'Présent'
    ABSENT = 'ABSENT', 'Absent'
    EN_RETARD = 'RETARD', 'En retard'
    JUSTIFIE = 'JUSTIFIE', 'Absent Justifié'

class PeriodeSession(models.TextChoices):
    MATIN = 'AM', 'Matin (8h - 12h)'
    APRES_MIDI = 'PM', 'Après-midi (14h - 18h)'

class TypeSession(models.TextChoices):
    THEORIE = 'THEORIE', 'Cours Théorique (Salle)'
    PRATIQUE = 'PRATIQUE', 'Atelier Pratique (Garage)'

class EchelleEvaluation(models.TextChoices):
    ACQUIS = 'A', 'Acquis'
    EN_COURS = 'ECA', 'En Cours d\'Acquisition'
    NON_ACQUIS = 'NA', 'Non Acquis'

class TypeArticle(models.TextChoices):
    PIECE_DETACHEE = 'PIECE', 'Pièce Détachée'
    CONSOMMABLE = 'CONSOMMABLE', 'Consommable (Huile, Liquide, Filtre)'
    OUTILLAGE = 'OUTIL', 'Petit Outillage d\'Atelier'

class StatutCommande(models.TextChoices):
    EN_ATTENTE = 'ATTENTE', 'En attente de validation'
    COMMANDEE = 'COMMANDEE', 'Commandé chez le fournisseur'
    RECUE = 'RECUE', 'Reçu / En Stock'
    ANNULLEE = 'ANNULLEE', 'Annulé'

class DestinationUsage(models.TextChoices):
    REPARATION_CLIENT = 'CLIENT', 'Réparation Client (Facturable)'
    EXERCICE_ETUDIANT = 'FORMATION', 'Exercice Pratique / Formation'
    PERTE_OU_CASSE = 'PERTE', 'Perte / Casse / Vol'

class TypeFacture(models.TextChoices):
    REPARATION_GARAGE = 'GARAGE', 'Réparation Automobile (Atelier)'
    FRAIS_SCOLARITE = 'ACADEMY', 'Frais de Scolarité / Formation'

class StatutFacture(models.TextChoices):
    BROUILLON = 'BROUILLON', 'Brouillon'
    IMPAYEE = 'IMPAYEE', 'Impayé'
    PARTIELLE = 'PARTIELLE', 'Payé Partiellement'
    PAYEE = 'PAYEE', 'Payé'
    ANNULEE = 'ANNULEE', 'Annulé / Avoir'

class ModePaiement(models.TextChoices):
    MOBILE_MONEY = 'MOBILE_MONEY', 'Mobile Money (Orange, MTN, Moov, Wave)'
    CARTE_BANCAIRE = 'CARTE', 'Carte Bancaire (Visa, Mastercard)'
    ESPECES = 'ESPECES', 'Espèces / Encaissé sur place'
    VIREMENT = 'VIREMENT', 'Virement Bancaire'


# =========================================================================
# 2. MODÈLES : MODULE GARAGE
# =========================================================================


class ProfilClient(models.Model):
    utilisateur = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profil_client', verbose_name="Utilisateur")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    adresse = models.TextField(blank=True, null=True, verbose_name="Adresse")
    # 🎯 Ajout de la photo optionnelle pour le client
    photo = models.ImageField(upload_to="clients_photos/", blank=True, null=True, verbose_name="Photo de profil (Optionnelle)")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")

    def __str__(self):
        return f"{self.utilisateur.get_full_name()} ({self.telephone})"



class FicheTravail(models.Model):
    type_document = models.CharField(max_length=10, choices=TypeDocument.choices, default=TypeDocument.DEVIS, verbose_name="Type de document")
    statut = models.CharField(max_length=10, choices=StatutVehicule.choices, default=StatutVehicule.DIAGNOSTIC, verbose_name="Statut du véhicule")
    vehicule = models.ForeignKey(Vehicule, on_delete=models.CASCADE, related_name='fiches_travail', verbose_name="Véhicule")
    description_panne = models.TextField(verbose_name="Description de la panne")
    notes_diagnostic = models.TextField(blank=True, null=True, verbose_name="Notes de diagnostic")
    
    # Corrections AUTH_USER_MODEL ici
    formateur_superviseur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='travaux_supervises', verbose_name="Formateur Superviseur")
    etudiants_assignes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='travaux_assignes', blank=True, verbose_name="Binôme / Groupe d'étudiants")
    
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    livraison_estimee = models.DateTimeField(blank=True, null=True, verbose_name="Date de livraison estimée")

    def __str__(self):
        return f"{self.get_type_document_display()} N° {self.id} - {self.vehicule.immatriculation}"



class LigneTravail(models.Model):
    fiche_travail = models.ForeignKey(FicheTravail, on_delete=models.CASCADE, related_name='lignes', verbose_name="Fiche de travail associée")
    designation = models.CharField(max_length=255, verbose_name="Désignation")
    quantite = models.DecimalField(max_digits=5, decimal_places=2, default=1.0, verbose_name="Quantité / Heures")
    prix_unitaire_ht = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Prix unitaire HT")
    taux_tva = models.DecimalField(max_digits=4, decimal_places=2, default=18.00, verbose_name="Taux TVA (%)")

    @property
    def total_ht(self):
        return self.quantite * self.prix_unitaire_ht




# =========================================================================
# 3. MODÈLES : MODULE SCOLARITÉ
# =========================================================================

class Promotion(models.Model):
    nom = models.CharField(max_length=100, verbose_name="Nom de la promotion")
    niveau = models.CharField(max_length=50, verbose_name="Niveau / Diplôme")
    date_debut = models.DateField(verbose_name="Date de début")
    date_fin = models.DateField(verbose_name="Date de fin")

    def __str__(self):
        return f"{self.nom} ({self.niveau})"



class ProfilEtudiant(models.Model):
    utilisateur = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profil_etudiant', verbose_name="Utilisateur")
    promotion = models.ForeignKey(Promotion, on_delete=models.PROTECT, related_name='etudiants', verbose_name="Promotion")
    matricule = models.CharField(max_length=20, unique=True, verbose_name="Matricule")
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    est_actif = models.BooleanField(default=True, verbose_name="Compte actif ?")

    def __str__(self):
        return f"[{self.matricule}] {self.utilisateur.get_full_name()}"



class Competence(models.Model):
    code = models.CharField(max_length=20, unique=True, verbose_name="Code Compétence")
    titre = models.CharField(max_length=255, verbose_name="Libellé de la compétence")
    categorie = models.CharField(max_length=100, verbose_name="Catégorie")

    def __str__(self):
        return f"{self.code} - {self.titre}"



class SessionPlanifiee(models.Model):
    titre = models.CharField(max_length=255, verbose_name="Titre du cours")
    type_session = models.CharField(max_length=15, choices=TypeSession.choices, default=TypeSession.THEORIE, verbose_name="Type de session")
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='sessions', verbose_name="Promotion")
    formateur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='sessions_enseignees', verbose_name="Formateur")
    date = models.DateField(verbose_name="Date")
    periode = models.CharField(max_length=2, choices=PeriodeSession.choices, verbose_name="Période")
    salle_ou_emplacement = models.CharField(max_length=50, blank=True, null=True, verbose_name="Lieu")

    class Meta:
        unique_together = ('date', 'periode', 'formateur')

    def __str__(self):
        return f"{self.date} - {self.titre}"



class Presence(models.Model):
    session = models.ForeignKey(SessionPlanifiee, on_delete=models.CASCADE, related_name='presences')
    etudiant = models.ForeignKey(ProfilEtudiant, on_delete=models.CASCADE, related_name='presences')
    statut = models.CharField(max_length=15, choices=StatutPresence.choices, default=StatutPresence.PRESENT)
    date_signature = models.DateTimeField(blank=True, null=True, verbose_name="Heure de signature")
    valide_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='presences_validees')

    class Meta:
        unique_together = ('session', 'etudiant')



class EvaluationCompetence(models.Model):
    etudiant = models.ForeignKey(ProfilEtudiant, on_delete=models.CASCADE, related_name='evaluations')
    competence = models.ForeignKey(Competence, on_delete=models.CASCADE, related_name='evaluations')
    resultat = models.CharField(max_length=5, choices=EchelleEvaluation.choices, default=EchelleEvaluation.NON_ACQUIS)
    
    # Correction de l'application cible : 'cfma_base.FicheTravail'
    fiche_travail = models.ForeignKey('cfma_base.FicheTravail', on_delete=models.SET_NULL, null=True, blank=True, related_name='evaluations_pedagogiques')
    evalue_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='evaluations_donnees')
    commentaires = models.TextField(blank=True, null=True)
    date_mise_a_jour = models.DateTimeField(auto_now=True)
    
    

    
#=========================================================================4. MODÈLES : MODULE STOCKS=========================================================================
# 
class Fournisseur(models.Model):
    nom_entreprise = models.CharField(max_length=150, verbose_name="Nom de l'entreprise")
    nom_contact = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nom du contact")
    telephone = models.CharField(max_length=20, verbose_name="Téléphone")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    adresse = models.TextField(blank=True, null=True, verbose_name="Adresse")
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def str(self):
        return self.nom_entreprise


class ArticleStock(models.Model):
    reference_sku = models.CharField(max_length=50, unique=True, verbose_name="Référence SKU")
    nom = models.CharField(max_length=200, verbose_name="Nom")
    type_article = models.CharField(max_length=15, choices=TypeArticle.choices, default=TypeArticle.PIECE_DETACHEE)
    quantite_en_stock = models.DecimalField(max_digits=8, decimal_places=2, default=0.00)
    alerte_stock_minimum = models.DecimalField(max_digits=6, decimal_places=2, default=2.00)
    prix_achat_ht = models.DecimalField(max_digits=10, decimal_places=2)
    prix_vente_ht = models.DecimalField(max_digits=10, decimal_places=2)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    def str(self):return self.nom
    
    
    
class CommandeApprovisionnement(models.Model):
    fournisseur = models.ForeignKey(Fournisseur, on_delete=models.PROTECT, related_name='commandes')
    numero_commande = models.CharField(max_length=50, unique=True)
    statut = models.CharField(max_length=15, choices=StatutCommande.choices, default=StatutCommande.EN_ATTENTE)
    cree_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='commandes_creees')
    date_creation = models.DateTimeField(auto_now_add=True)
    date_reception = models.DateTimeField(blank=True, null=True)
    


class LigneCommandeApprovisionnement(models.Model):
    commande_approvisionnement = models.ForeignKey(CommandeApprovisionnement, on_delete=models.CASCADE, related_name='lignes')
    article = models.ForeignKey(ArticleStock, on_delete=models.PROTECT)
    quantite_commandee = models.DecimalField(max_digits=8, decimal_places=2)  # Déplacé sur sa propre ligne
    prix_achat_negocie_ht = models.DecimalField(max_digits=10, decimal_places=2)

    


class MouvementStock(models.Model):
    article = models.ForeignKey(ArticleStock, on_delete=models.CASCADE, related_name='mouvements')
    quantite = models.DecimalField(max_digits=8, decimal_places=2)
    destination = models.CharField(max_length=15, choices=DestinationUsage.choices)
    
    # Corrections des applications cibles : 'cfma_base.X'
    fiche_travail = models.ForeignKey('cfma_base.FicheTravail', on_delete=models.SET_NULL, null=True, blank=True, related_name='consommations_stock')
    session_planifiee = models.ForeignKey('cfma_base.SessionPlanifiee', on_delete=models.SET_NULL, null=True, blank=True, related_name='consommations_stock')
    enregistre_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date_creation = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        # 1. Sauvegarde d'abord le mouvement en base
        super().save(*args, **kwargs)
                
        # 3. Recalcule la quantité totale de l'article lié
        total = self.article.mouvements.aggregate(Sum('quantite'))['quantite__sum'] or 0.00
        
        # 4. Met à jour et enregistre la fiche de l'article
        self.article.quantite_en_stock = total
        self.article.save()
    
    
    
    
#=========================================================================5. MODÈLES : MODULE FACTURATION=========================================================================

class Facture(models.Model):
    numero_facture = models.CharField(max_length=50, unique=True, verbose_name="Numéro de Facture")
    type_facture = models.CharField(max_length=10, choices=TypeFacture.choices, verbose_name="Type de Facture")
    statut = models.CharField(max_length=15, choices=StatutFacture.choices, default=StatutFacture.BROUILLON, verbose_name="Statut")
    destinataire = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='factures', verbose_name="Destinataire")
    
    # Corrections des applications cibles : 'cfma_base.X'
    fiche_travail = models.OneToOneField('cfma_base.FicheTravail', on_delete=models.SET_NULL, null=True, blank=True, related_name='facture')
    profil_etudiant = models.ForeignKey('cfma_base.ProfilEtudiant', on_delete=models.SET_NULL, null=True, blank=True, related_name='factures_scolarite')
    date_emission = models.DateField(verbose_name="Date d'émission")
    date_echeance = models.DateField(verbose_name="Date d'échéance")
    remise_globale = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    @property
    def total_ht(self):
        return sum(ligne.sous_total_ht for ligne in self.lignes.all())
     
    @property
    def total_tva(self):
        return sum(ligne.sous_total_tva for ligne in self.lignes.all())
        
        
    @property
    def total_ttc(self):
        return (self.total_ht + self.total_tva) - self.remise_globale
        
        
        
    @property
    def montant_paye(self):
        return sum(p.montant for p in self.paiements.filter(est_reussi=True))
        
        
    @property
    def solde_restant(self):
        return self.total_ttc - self.montant_paye
        
    


class LigneFacture(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='lignes')
    designation = models.CharField(max_length=255)
    quantite = models.DecimalField(max_digits=6, decimal_places=2, default=1.00)
    prix_unitaire_ht = models.DecimalField(max_digits=10, decimal_places=2)
    taux_tva = models.DecimalField(max_digits=4, decimal_places=2, default=18.00)
    
        
    @property
    def sous_total_ht(self):
        return self.quantite * self.prix_unitaire_ht
        
        
    @property
    def sous_total_tva(self):
        return self.sous_total_ht * (self.taux_tva / 100)
        
    
class TransactionPaiement(models.Model):
    facture = models.ForeignKey(Facture, on_delete=models.CASCADE, related_name='paiements')
    mode_paiement = models.CharField(max_length=20, choices=ModePaiement.choices)
    montant = models.DecimalField(max_digits=10, decimal_places=2)
    reference_paystack = models.CharField(max_length=100, unique=True, blank=True, null=True)
    dump_reponse_paystack = models.JSONField(blank=True, null=True)
    est_reussi = models.BooleanField(default=False)
    date_transaction = models.DateTimeField(auto_now_add=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        facture_associee = self.facture
        if facture_associee.solde_restant <= 0:
            facture_associee.statut = StatutFacture.PAYEE
        elif facture_associee.montant_paye > 0:
            facture_associee.statut = StatutFacture.PARTIELLE
        else:
            facture_associee.statut = StatutFacture.IMPAYEE
            facture_associee.save()



















