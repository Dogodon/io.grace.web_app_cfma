
# cfma_base/urls.py
from django.urls import path
from . import views

app_name = 'cfma_base'


from django.urls import path
from . import views  # Import de vos vues

# cfma_base/urls.py
from django.urls import path
from . import views

app_name = 'cfma_base'




urlpatterns = [
    # Page d'accueil de l'application
    path('', views.home, name='home'), 
    
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


