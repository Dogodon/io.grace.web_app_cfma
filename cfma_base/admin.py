from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, ProfilClient, Vehicule, FicheTravail, LigneTravail,
    Promotion, ProfilEtudiant, Competence, SessionPlanifiee, Presence, EvaluationCompetence,
    Fournisseur, ArticleStock, CommandeApprovisionnement, LigneCommandeApprovisionnement, MouvementStock,
    Facture, LigneFacture, TransactionPaiement
)

from django.contrib import admin
from .models import RDVDiagnostic

 # sfma_base/admin.py
from django.contrib.admin.models import LogEntry, CHANGE
# sfma_base/admin.py
from django.contrib import admin
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from django.utils.html import format_html
from django.shortcuts import render
from django.urls import path
from django.db.models import Count
from .models import ProfilClient, Vehicule, MouvementVehicule











from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    User, ProfilClient, Vehicule, FicheTravail, LigneTravail,
    Promotion, ProfilEtudiant, Competence, SessionPlanifiee, Presence, EvaluationCompetence,
    Fournisseur, ArticleStock, CommandeApprovisionnement, LigneCommandeApprovisionnement, MouvementStock,
    Facture, LigneFacture, TransactionPaiement
)








from .models import ElementService, Actualite, PartenaireContact, FormationCatalogue
from django.contrib import admin
from .models import GalerieCommentaireClient






















# =========================================================================
# 📊 1. DÉFINITION DU SITE ADMIN AVEC LE TABLEAU DE BORD (SANS RE-LIAISON)
# =========================================================================
class SFMAGarageAdminSite(admin.AdminSite):
    site_header = "SFMA Orange Administration"
    
    def index(self, request, extra_context=None):
        extra_context = extra_context or {}
        
        # Statistiques KPIs principales
        extra_context['total_clients'] = ProfilClient.objects.count()
        extra_context['en_atelier'] = MouvementVehicule.objects.filter(statut='ATELIER').count()
        extra_context['restitues'] = MouvementVehicule.objects.filter(statut='RESTITUE').count()
        
        # Suivi de l'activité (Faits et gestes)
        extra_context['recents_logs'] = LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:10]
        
        # Données du Graphique Chart.js
        carburant_data = MouvementVehicule.objects.values('niveau_carburant_entree').annotate(total=Count('id'))
        extra_context['graphe_labels'] = [item['niveau_carburant_entree'] for item in carburant_data]
        extra_context['graphe_valeurs'] = [item['total'] for item in carburant_data]
        
        return super().index(request, extra_context)


# Interception propre du site par défaut de Django
admin.site.__class__ = SFMAGarageAdminSite


# =========================================================================
# 🕵️‍♂️ 2. TRAÇABILITÉ AUTOMATIQUE DES CONSULTATIONS (VUES)
# =========================================================================
class LogViewAdmin(admin.ModelAdmin):
    """Enregistre un fait et geste dès qu'un utilisateur ouvre un élément"""
    def change_view(self, request, object_id, form_url='', extra_context=None):
        obj = self.get_object(request, object_id)
        if obj and request.user.is_authenticated:
            LogEntry.objects.log_action(
                user_id=request.user.id,
                content_type_id=admin.options.get_content_type_for_model(obj).id,
                object_id=obj.id,
                object_repr=str(obj),
                action_flag=CHANGE,
                change_message="A consulté la fiche détaillée de l'élément (Vue)."
            )
        return super().change_view(request, object_id, form_url, extra_context)


# =========================================================================
# 🚗 3. ENREGISTREMENTS UNIQUES DES MODÈLES (AUCUN DOUBLON POSSIBLE)
# =========================================================================



# =========================================================================
# 0. CONFIGURATION DE L'UTILISATEUR PERSONNALISÉ
# =========================================================================
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """Intègre le champ 'role' dans l'administration des utilisateurs."""
    fieldsets = UserAdmin.fieldsets + (
        ('Informations de Rôle', {'fields': ('role',)}),
    )
    list_display = ['username', 'email', 'first_name', 'last_name', 'role', 'is_staff']
    list_filter = ['role', 'is_staff', 'is_superuser', 'is_active']



@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('action_time', 'user', 'content_type', 'object_repr', 'get_action_flag_badge')
    list_filter = ('action_time', 'user', 'action_flag')
    search_fields = ('object_repr', 'change_message')
    date_hierarchy = 'action_time'

    def get_action_flag_badge(self, obj):
        if obj.action_flag == ADDITION:
            return format_html('<span class="badge" style="background-color: #28a745; color: white;">Ajout</span>')
        elif obj.action_flag == CHANGE:
            return format_html('<span class="badge" style="background-color: #FF6600; color: white;">Modif</span>')
        elif obj.action_flag == DELETION:
            return format_html('<span class="badge" style="background-color: #dc3545; color: white;">Suppr</span>')
        return "Inconnu"
    get_action_flag_badge.short_description = "Action"


@admin.register(ProfilClient)
class ProfilClientAdmin(LogViewAdmin):
    list_display = ('get_nom_complet', 'telephone', 'adresse', 'date_creation')
    search_fields = ('utilisateur__first_name', 'utilisateur__last_name', 'telephone')

    def get_nom_complet(self, obj):
        if obj.utilisateur:
            return obj.utilisateur.get_full_name() or obj.utilisateur.username
        return "Aucun utilisateur lié"
    get_nom_complet.short_description = "Nom du Client"










@admin.register(RDVDiagnostic)
class RDVDiagnosticAdmin(admin.ModelAdmin):
    list_display = ('nom', 'telephone', 'email', 'date_souhaitee', 'date_creation')
    list_filter = ('date_souhaitee', 'date_creation')
    search_fields = ('nom', 'telephone', 'email')








from .models import ElementService, Actualite, PartenaireContact, FormationCatalogue, GalerieCommentaireClient, GalerieCommentaireEvenement

# ==========================================================
# 🌟 NOUVEAUX MENUS SÉPARÉS POUR LES GALERIES CARROUSEL
# ==========================================================


@admin.register(GalerieCommentaireClient)
class GalerieCommentaireClientAdmin(admin.ModelAdmin):
    list_display = ('auteur', 'titre_prestation', 'statut_vehicule')
    search_fields = ('auteur', 'titre_prestation', 'commentaire')



@admin.register(GalerieCommentaireEvenement)
class GalerieCommentaireEvenementAdmin(admin.ModelAdmin):
    list_display = ('acteurs', 'titre_evenement', 'statut_evenement')
    search_fields = ('acteurs', 'titre_evenement', 'commentaire')
    list_filter = ('statut_evenement',)



from django.contrib import admin
from .models import GalerieCFMA

@admin.register(GalerieCFMA)
class GalerieCFMAAdmin(admin.ModelAdmin):
    # Configuration de l'affichage dans la liste
    list_display = ('nom_patron', 'str_aperçu_histoire')
    
    # Organisation du formulaire d'édition par onglets/sections
    fieldsets = (
        ("👨‍💼 Équipe Dirigeante", {
            'fields': ('nom_patron', 'biographie_patron')
        }),
        ("🏫 Présentation du Centre", {
            'fields': ('biographie_cfma',)
        }),
        ("📸 Carrousel Photo (1 à 5)", {
            'fields': ('image1', 'image2', 'image3', 'image4', 'image5'),
            'description': "Ajoutez les visuels d'illustration pour le carrousel de la page À Propos. La première image est requise."
        }),
    )

    def str_aperçu_histoire(self, obj):
        if obj.biographie_cfma:
            return obj.biographie_cfma[:60] + "..."
        return "Non renseignée"
    str_aperçu_histoire.short_description = "Aperçu de l'histoire CFMA"



@admin.register(PartenaireContact)
class PartenaireContactAdmin(admin.ModelAdmin):
    list_display = ('nom_societe', 'telephone_pro', 'email_pro')
    search_fields = ('nom_societe', 'email_pro')

























########################
# sfma_base/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import MouvementVehicule

@admin.register(MouvementVehicule)
class MouvementVehiculeAdmin(admin.ModelAdmin):
    # Colonnes affichées dans la liste globale
    list_display = ('get_statut_badge', 'get_immatriculation', 'depose_nom', 'date_entree', 'get_preview_plaque', 'date_sortie')
    list_filter = ('statut', 'date_entree', 'niveau_carburant_entree')
    search_fields = ('depose_nom', 'immatriculation_manuelle', 'vehicule_connu__immatriculation', 'retrait_nom')
    
    # Organisation du formulaire d'édition par blocs (Fieldsets)
    fieldsets = (
        ("Statut du Flux", {
            'fields': ('statut',)
        }),
        ("Étape 1 : Entrée / Déposant", {
            'fields': ('depose_nom', 'depose_prenom', 'depose_travail', 'depose_image', 'date_entree')
        }),
        ("Détails du Véhicule", {
            'fields': ('vehicule_connu', 'immatriculation_manuelle', 'photo_plaque', 'photo_voiture', 'kilometrage_entree', 'niveau_carburant_entree', 'observations_dommages')
        }),
        ("Étape 2 : Sortie / Récupérateur", {
            'fields': ('retrait_nom', 'retrait_prenom', 'retrait_travail', 'retrait_image', 'date_sortie', 'kilometrage_sortie')
        }),
    )

    # Fonction pour afficher l'immatriculation qu'elle soit manuelle ou liée au modèle Véhicule
    def get_immatriculation(self, obj):
        if obj.vehicule_connu:
            return obj.vehicule_connu.immatriculation
        return obj.immatriculation_manuelle or "Non renseignée"
    get_immatriculation.short_description = "Immatriculation"

    # 🎯 CORRECTION : Utilisation stricte des arguments de formatage
    def get_statut_badge(self, obj):
        if obj.statut == 'ATELIER':
            return format_html(
                '<span class="badge badge-warning" style="background-color: #FF6600 !important; color: white;">{}</span>', 
                "En Atelier"
            )
        return format_html(
            '<span class="badge badge-success" style="background-color: #28a745 !important; color: white;">{}</span>', 
            "Restitué"
        )
    get_statut_badge.short_description = "Statut"

    # 🎯 CORRECTION : Sécurisation de l'affichage de la miniature de la plaque
    def get_preview_plaque(self, obj):
        if obj.photo_plaque:
            return format_html(
                '<img src="{}" style="width: 60px; height: auto; border-radius: 4px; border: 1px solid #ddd;" />', 
                obj.photo_plaque.url
            )
        return "Aucune photo"
    get_preview_plaque.short_description = "Aperçu Plaque"



# =========================================================================
# 1. MODULE GARAGE (ATELIER)
# =========================================================================
class LigneTravailInline(admin.TabularInline):
    model = LigneTravail
    extra = 1

@admin.register(FicheTravail)
class FicheTravailAdmin(admin.ModelAdmin):
    list_display = ['id', 'type_document', 'statut', 'vehicule', 'formateur_superviseur', 'date_creation']
    list_filter = ['type_document', 'statut', 'date_creation']
    search_fields = ['vehicule__immatriculation', 'vehicule__proprietaire__utilisateur__last_name']
    filter_horizontal = ['etudiants_assignes']
    inlines = [LigneTravailInline]

#admin.site.register(ProfilClient)
admin.site.register(Vehicule)


# =========================================================================
# 2. MODULE SCOLARITÉ (FORMATION)
# =========================================================================
class PresenceInline(admin.TabularInline):
    model = Presence
    extra = 0

@admin.register(SessionPlanifiee)
class SessionPlanifieeAdmin(admin.ModelAdmin):
    list_display = ['date', 'periode', 'titre', 'type_session', 'promotion', 'formateur']
    list_filter = ['type_session', 'periode', 'date']
    search_fields = ['titre', 'formateur__last_name']
    inlines = [PresenceInline]

@admin.register(ProfilEtudiant)
class ProfilEtudiantAdmin(admin.ModelAdmin):
    list_display = ['matricule', 'utilisateur', 'promotion', 'est_actif']
    search_fields = ['matricule', 'utilisateur__last_name', 'utilisateur__first_name']
    list_filter = ['promotion', 'est_actif']

admin.site.register(Promotion)
admin.site.register(Competence)
admin.site.register(EvaluationCompetence)


# =========================================================================
# 3. MODULE STOCKS (INVENTAIRE)
# =========================================================================
class LigneCommandeInline(admin.TabularInline):
    model = LigneCommandeApprovisionnement
    extra = 1

@admin.register(ArticleStock)
class ArticleStockAdmin(admin.ModelAdmin):
    list_display = ['reference_sku', 'nom', 'type_article', 'quantite_en_stock', 'alerte_stock_minimum', 'est_en_rupture_critique']
    list_filter = ['type_article']
    search_fields = ['reference_sku', 'nom']

    @admin.display(boolean=True, description="Rupture critique ?")
    def est_en_rupture_critique(self, obj):
        """
        Calcule instantanément si la quantité disponible est inférieure 
        ou égale au seuil de sécurité minimum configuré.
        """
        return obj.quantite_en_stock <= obj.alerte_stock_minimum


@admin.register(CommandeApprovisionnement)
class CommandeApprovisionnementAdmin(admin.ModelAdmin):
    list_display = ['numero_commande', 'fournisseur', 'statut', 'date_creation']
    list_filter = ['statut', 'date_creation']
    inlines = [LigneCommandeInline]

admin.site.register(Fournisseur)
admin.site.register(MouvementStock)


# =========================================================================
# 4. MODULE FACTURATION & COMPTABILITÉ
# =========================================================================
class LigneFactureInline(admin.TabularInline):
    model = LigneFacture
    extra = 1

class TransactionPaiementInline(admin.TabularInline):
    model = TransactionPaiement
    extra = 0
    readonly_fields = ['date_transaction']

@admin.register(Facture)
class FactureAdmin(admin.ModelAdmin):
    list_display = ['numero_facture', 'type_facture', 'destinataire', 'statut', 'total_ttc', 'solde_restant', 'date_emission']
    list_filter = ['type_facture', 'statut', 'date_emission']
    search_fields = ['numero_facture', 'destinataire__last_name']
    inlines = [LigneFactureInline, TransactionPaiementInline]











# sfma_base/admin.py (Tout en bas)

admin.site.register(ElementService)
#admin.site.register(PartenaireContact)
admin.site.register(FormationCatalogue)

@admin.register(Actualite)
class ActualiteAdmin(admin.ModelAdmin):
    list_display = ['titre', 'date_publication', 'est_epinglé']
    list_filter = ['est_epinglé', 'date_publication']


