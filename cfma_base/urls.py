
# cfma_base/urls.py
from django.urls import path
from . import views

app_name = 'cfma_base'


from django.urls import path
from . import views  # Import de vos vues

# cfma_base/urls.py
from django.urls import path
from . import views


from django.urls import path
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse


app_name = 'cfma_base'


# 1. Définition des pages statiques de votre Centre de Formation
class StaticViewSitemap(Sitemap):
    changefreq = "weekly"  # Fréquence de mise à jour des pages
    priority = 0.8         # Importance des pages (de 0.0 à 1.0)

    def items(self):
        # Mettez ici les "names" de vos vues définies dans vos urls.py
        return ['home', 'actualites', 'services', 'formations', 'apropos']

    def location(self, item):
        return reverse(item)

# 2. Dictionnaire des sitemaps
sitemaps = {
    'static': StaticViewSitemap,
}




urlpatterns = [
    # Page d'accueil de l'application
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    path('', views.home, name='home'), 
    

    #path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),


    # Fil de commentaires global autonome (sans clé étrangère)
    path('galeries-commentaires-clients/', views.galeries_commentaires_clients, name='galeries_commentaires_clients'),
    

    path('galeries-commentaires-evenements/', views.galeries_commentaires_evenements, name='galeries_commentaires_evenements'),
    path('galeries-commentaires-evenements/', views.galeries_commentaires_evenements, name='galeries_commentaires_evenements'),
    path('a-propos/', views.a_propos, name='a_propos'),



    path('mouvements/', views.dashboard_mouvements, name='dashboard_mouvements'),
    path('mouvements/entree/', views.enregistrer_entree, name='enregistrer_entree'),
    path('mouvements/sortie/<int:pk>/', views.enregistrer_sortie, name='enregistrer_sortie'),



    # Prise de rendez-vous
    path('diagnostic/rdv/', views.prendre_rdv_diagnostic, name='prendre_rdv_diagnostic'),
]


