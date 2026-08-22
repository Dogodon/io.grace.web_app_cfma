# sfma_base/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ProfilClient, ProfilEtudiant, Promotion
from django import forms
from .models import ProfilClient, Vehicule

""" 

(venv) (base) pcmarket@192 website_sfma % python manage.py createsuperuser
Username: admin
Email address: admin@sfma.ci
Password: 
Password (again): 
Superuser created successfully.
(venv) (base) pcmarket@192 website_sfma % 

 """

class InscriptionForm(UserCreationForm):
    """Formulaire d'inscription universel créant les profils dépendants du rôle."""
    email = forms.EmailField(required=True, label="Adresse Email")
    telephone = forms.CharField(max_length=20, required=True, label="Téléphone")
    adresse = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), required=False, label="Adresse (Clients)")
    
    # Pour les étudiants uniquement
    promotion = forms.ModelChoiceField(queryset=Promotion.objects.all(), required=False, label="Promotion (Apprenants)")
    matricule = forms.CharField(max_length=20, required=False, label="Matricule (Apprenants)")

    class Meta(UserCreationForm.Meta):
        model = User
        # ⚠️ CRUCIAL : Il faut inclure TOUS les champs du formulaire ici pour que cleaned_data les capture !
        fields = (
            'username', 'first_name', 'last_name', 'email', 'role', 
            'telephone', 'adresse', 'promotion', 'matricule'
        )

    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        telephone = cleaned_data.get('telephone')
        
        # Validation du rôle
        if not role:
            self.add_error('role', "Veuillez sélectionner un rôle.")
            return cleaned_data
            
        # Validations strictes selon le rôle choisi
        if role == User.Roles.CLIENT and not telephone:
            self.add_error('telephone', "Le numéro de téléphone est obligatoire pour un client.")
        
        if role == User.Roles.APPRENANT:
            if not cleaned_data.get('promotion'):
                self.add_error('promotion', "La promotion est requise pour un apprenant.")
            if not cleaned_data.get('matricule'):
                self.add_error('matricule', "Le matricule est requis pour un apprenant.")
                
        return cleaned_data



    def save(self, commit=True):
        # 1. On laisse UserCreationForm créer et sauvegarder l'utilisateur proprement en BDD
        # Cela gère le hachage du mot de passe et l'écriture de manière 100% sécurisée.
        user = super().save(commit=commit)
        
        # 2. On met à jour l'email et le rôle du personnel si commit est True
        if commit:
            user.email = self.cleaned_data.get('email')
            
            if user.role in [User.Roles.PATRON, User.Roles.SECRETAIRE, User.Roles.COMMERCIAL, User.Roles.INFORMATICIEN]:
                user.is_staff = True
                
            user.save() # On applique les modifications d'email et de statut admin

            # 3. Création automatique des profils secondaires associés
            if user.role == User.Roles.CLIENT:
                ProfilClient.objects.get_or_create(
                    utilisateur=user,
                    defaults={
                        'telephone': self.cleaned_data.get('telephone'),
                        'adresse': self.cleaned_data.get('adresse')
                    }
                )
            elif user.role == User.Roles.APPRENANT:
                ProfilEtudiant.objects.get_or_create(
                    utilisateur=user,
                    defaults={
                        'promotion': self.cleaned_data.get('promotion'),
                        'matricule': self.cleaned_data.get('matricule'),
                        'telephone': self.cleaned_data.get('telephone')
                    }
                )
        return user




from django import forms

class DiagnosticRDVForm(forms.Form):
    nom = forms.CharField(
        max_length=100, 
        label="Nom complet",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Jean Dupont'})
    )
    email = forms.EmailField(
        label="Adresse Email",
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Ex: jean.dupont@email.com'})
    )
    telephone = forms.CharField(
        max_length=20, 
        label="Numéro de Téléphone",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: +33 6 12 34 56 78'})
    )
    date_souhaitee = forms.DateTimeField(
        label="Date et Heure souhaitées",
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )





























# sfma_base/forms.py
from django import forms
from .models import MouvementVehicule

class EntreeVehiculeForm(forms.ModelForm):
    class Meta:
        model = MouvementVehicule
        fields = [
            'vehicule_connu', 'immatriculation_manuelle', 'photo_plaque', 'photo_voiture',
            'depose_nom', 'depose_prenom', 'depose_travail', 'depose_image',
            'kilometrage_entree', 'niveau_carburant_entree', 'observations_dommages'
        ]
        widgets = {
            'observations_dommages': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Ex: Rayure portière droite, pare-chocs fissuré...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})


class SortieVehiculeForm(forms.ModelForm):
    class Meta:
        model = MouvementVehicule
        fields = ['retrait_nom', 'retrait_prenom', 'retrait_travail', 'retrait_image', 'kilometrage_sortie']
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        # Rendre ces champs obligatoires uniquement au moment de la sortie effective
        self.fields['retrait_nom'].required = True
        self.fields['kilometrage_sortie'].required = True









""" class DiagnosticRDVForm(forms.Form):
    # Correction ici : max_length au lieu de max_value
    nom = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control'}))
    
    # Correction ici également
    telephone = forms.CharField(max_length=20, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    date_souhaitee = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}))

 """



class RapideClientForm(forms.ModelForm):
    class Meta:
        model = ProfilClient
        # 🌟 Nettoyage complet : on garde UNIQUEMENT les vrais champs du modèle ProfilClient
        fields = ['telephone', 'adresse']
        widgets = {
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Adresse (Optionnelle)'}),
        }

class RapideVehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        # 🌟 Nettoyage : On garde UNIQUEMENT 'immatriculation' (votre modèle Vehicule n'a pas de champ image)
        fields = ['immatriculation']
        widgets = {
            'immatriculation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: AA-123-BB'}),
        }


""" class RapideClientForm(forms.ModelForm):
    class Meta:
        model = ProfilClient
        fields = ['nom', 'prenoms', 'telephone', 'adresse', 'image']
        widgets = {
           # 'nom': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nom'}),
            #'prenoms': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Prénoms'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Téléphone'}),
            'adresse': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Adresse (Optionnelle)'}),
            #'image': forms.FileInput(attrs={'class': 'form-control'}),
        }

class RapideVehiculeForm(forms.ModelForm):
    class Meta:
        model = Vehicule
        fields = ['immatriculation', 'image']
        widgets = {
            'immatriculation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: AA-123-BB'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
        }
 """