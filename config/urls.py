"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""






# config/urls.py
from django.contrib import admin
from django.urls import path,include
from cfma_base import views  # Import global unique pour nettoyer l'espace de nom
from django.contrib.auth.views import LogoutView
from django.conf.urls.static import static
from django.conf import settings
from cfma_base.views import * #votre_vue_1, votre_vue_2 # Importez uniquement les vues dont vous avez besoin pour vos routes
# OU BIEN :

from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views

#app_name = 'cfma_base'


from django.contrib import admin
from django.urls import path, include
from django.shortcuts import reverse                 # <-- Règle l'erreur « reverse » n’est pas défini
from django.contrib.sitemaps import Sitemap          # <-- Règle l'erreur « Sitemap » n’est pas défini
from django.contrib.sitemaps.views import sitemap



# 1. Définition des pages statiques de votre Centre de Formation
class StaticViewSitemap(Sitemap):
    changefreq = "weekly"  # Fréquence de mise à jour des pages
    priority = 0.8         # Importance des pages (de 0.0 à 1.0)

    def items(self):
        # Mettez ici les "names" de vos vues définies dans vos urls.py
        return ['cfma_base:home', 'catalogue_actualites', 'catalogue_services', 'catalogue_formations', 'catalogue_contact']

    def location(self, item):
        return reverse(item)

# 2. Dictionnaire des sitemaps
sitemaps = {
    'static': StaticViewSitemap,
}

""" class StaticViewSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        # On sécurise en ne mettant que l'accueil pour le premier test
        return ['cfma_base:home']

    def location(self, item):
        return reverse(item)

sitemaps = {
    'static': StaticViewSitemap,
}
 """


urlpatterns = [
    # On ajoute les deux versions pour être 100% sûr que Django intercepte la demande
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('sitemap.xml/', sitemap, {'sitemaps': sitemaps}), 
    
    path('admin/', admin.site.urls),
    #path('', include('cfma_base'))
    path('', include('cfma_base.urls')),  # Notez bien le ".urls" à la fin


    # Page d'accueil du site
    path('', views.home, name='home'), 



    path('prendre-rdv-diagnostic/', views.prendre_rdv_diagnostic, name='prendre_rdv_diagnostic'),





    # Authentification et gestion des comptes
    path('connexion/', views.ConnexionPersonnaliseeView.as_view(), name='login'),
    #path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    path('deconnexion/', LogoutView.as_view(next_page='/'), name='logout'),
    path('inscription/', views.inscription_universelle, name='inscription'),
    path('portail/', views.redirection_portail, name='redirection_portail'),






    path('formations/', views.page_formations, name='catalogue_formations'),
    path('services/', views.page_services, name='catalogue_services'),
    path('actualites/', views.page_actualites, name='catalogue_actualites'),
    path('contact/', views.page_contact, name='catalogue_contact'),








    # =========================================================================
    # PASSERELLE PAYSTACK & CONFIGURATIONS FINANCIÈRES
    # =========================================================================
    path('facturation/payer/<int:facture_id>/', views.initialiser_paiement_paystack, name='initialiser_paiement'),
    path('facturation/verifier-paiement/', views.verifier_paiement_paystack, name='verifier_paiement'),
    path('atelier/convertir-or/<int:fiche_id>/', views.convertir_devis_en_or, name='convertir_en_or'),
    path('facturation/telecharger-pdf/<int:facture_id>/', views.generer_pdf_facture, name='telecharger_facture_pdf'),

    # =========================================================================
    # MODULE GARAGE & ATELIER (GMAO)
    # =========================================================================
    # Clients & Véhicules
    path('garage/clients/', views.liste_clients_vehicules, name='liste_clients_vehicules'),
    path('garage/clients/<int:client_id>/ajouter-vehicule/', views.ajouter_vehicule, name='ajouter_vehicule'),
    
    # Suivi Kanban Atelier
    path('garage/atelier/tableau-bord/', views.tableau_bord_atelier, name='tableau_bord_atelier'),
    path('garage/atelier/fiche/<int:fiche_id>/changer-statut/', views.changer_statut_vehicule, name='changer_statut_vehicule'),
    
    # Devis & Ordres de Réparation
    path('garage/vehicule/<int:vehicule_id>/creer-fiche/', views.creer_fiche_travail, name='creer_fiche_travail'),
    path('garage/fiche/<int:fiche_id>/', views.details_fiche_travail, name='details_fiche_travail'),

    # =========================================================================
    # MODULE SCOLARITÉ (LMS)
    # =========================================================================
    # Promotions & Étudiants
    path('scolarite/promotions/', views.liste_promotions, name='liste_promotions'),
    path('scolarite/promotions/<int:promotion_id>/apprenants/', views.trombinoscope_promotion, name='trombinoscope_promotion'),
    
    # Feuilles d'émargement (Présences)
    path('scolarite/session/<int:session_id>/presence/', views.feuille_presence_session, name='feuille_presence_session'),
    path('scolarite/session/<int:session_id>/presence/enregistrer/', views.sauvegarder_emargement, name='sauvegarder_emargement'),
    
    # Livret d'évaluation de compétences
    path('scolarite/apprenant/<int:etudiant_id>/competences/', views.evaluation_competences_etudiant, name='evaluation_competences_etudiant'),
    path('scolarite/apprenant/<int:etudiant_id>/competences/<int:competence_id>/evaluer/', views.evaluer_competence, name='evaluer_competence'),

    # =========================================================================
    # MODULE STOCKS & LOGISTIQUE
    # =========================================================================
    # Consultation et mouvements physiques
    path('stock/inventaire/', views.inventaire_stock, name='inventaire_stock'),
    path('stock/article/<int:article_id>/sortir/', views.sortir_article_stock, name='sortir_article_stock'),
    
    # Gestion des commandes fournisseurs
    path('stock/commandes/creer/', views.creer_bon_commande, name='creer_bon_commande'),
    path('stock/commandes/<int:commande_id>/lignes/', views.editer_lignes_commande, name='editer_lignes_commande'),
    path('stock/commandes/<int:commande_id>/receptionner/', views.receptionner_commande, name='receptionner_commande'),

    # =========================================================================
    # JOURNAL DE FACTURATION & COMPTABILITÉ COMPTOIR
    # =========================================================================
    # Journal & Émission
    path('facturation/journal/', views.journal_facturation, name='journal_facturation'),
    path('facturation/emettre/', views.emettre_facture, name='emettre_facture'),
    path('facturation/<int:facture_id>/lignes/', views.editer_lignes_facture, name='editer_lignes_facture'),
    
    # Encaissement comptoir
    path('facturation/<int:facture_id>/encaisser/', views.enregistrer_paiement_manuel, name='enregistrer_paiement_manuel'),
    
    # Indicateurs KPI pour la direction (Patron)
    path('facturation/indicateurs/', views.indicateurs_financiers, name='indicateurs_financiers'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()

# Ajout obligatoire pour servir les fichiers médias en développement local
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



