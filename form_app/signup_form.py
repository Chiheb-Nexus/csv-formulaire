from django import forms
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from form_app import account_models


class RegistrationForm(forms.Form):
    """Formulaire d'inscription d'utilisateur"""

    username    = forms.CharField(label=_("Nom d'utilisateur"), min_length=4, max_length=150,
                    required=True, 
                    validators=[
                        RegexValidator(
                            '[a-zA-Z0-9]{4,}', 
                            message=_('Mot de passe doit être une combinison de charactères'
                                      ' et des chiffres.'))
                    ],
                    widget=forms.TextInput(attrs={'placeholder': "*nom d'utilisateur", 'class': 'form-control'}),
                    help_text=_('Mot de passe doit être une combinison de charactères et des chiffres.'))

    last_name   = forms.CharField(label=_('Nom'), max_length=150, required=False,
                    validators=[
                        RegexValidator(
                            '[a-zA-Z ]+',
                            message=_('Nom doit être une combinaison de charactères et "espace"')
                        )
                    ],
                    help_text = _('Nom doit être une combinaison de charactères et "espace"'),
                    widget=forms.TextInput(attrs={'placeholder': 'Nom', 'class': 'form-control'})
                 )
    first_name  = forms.CharField(label=_('Prénom'), max_length=150, required=False,
                    validators=[
                        RegexValidator(
                            '[a-zA-Z ]+',
                            message=_('Prénom doit être une combinaison de charactères et "espace"')
                        )
                    ],
                    help_text = _('Prénom doit être une combinaison de charactères et "espace"'),
                    widget=forms.TextInput(attrs={'placeholder': 'prénom', 'class': 'form-control'})
                )
    email       = forms.EmailField(max_length=254, required=True,
                    widget=forms.TextInput(attrs={'placeholder': '*example@dmain.com', 'class': 'form-control'}))
    password1   = forms.CharField(label=_('Mot de passe'), min_length=6,
                    widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    password2   = forms.CharField(label=_('Confirmer mot de passe'), min_length=6,
                    widget=forms.PasswordInput(attrs={'class': 'form-control'}), required=True)
    birth_date  = forms.DateField(
                    required=False, help_text=_('Nno requis. Format = YYYY-MM-DD'),
                    widget=forms.TextInput(attrs={'id': 'date', 'placeholder':'YYYY-MM-DD', 'class': 'form-control'}))
    info = forms.CharField(label=_('Bio'), required=False, 
                    widget=forms.Textarea(attrs={'placeholder': _('text...'), 'class': 'form-control', 'rows': 5}))

    def __init__(self, *args, **kwargs):
        '''Surcharger les attributes de UserCreationForm et ajouter des placeholder'''

        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = _('* username')
        self.fields['password1'].widget.attrs['placeholder'] = _('* password')
        self.fields['password2'].widget.attrs['placeholder'] = _('* confirm password')
        self.fields['password1'].help_text =  _(
            'Votre mot de passe ne peut pas trop ressembler à vos autres informations personnelles,'
            ' doit contenir au minimum 8 caractères,'
            ' ne peut pas être un mot de passe couramment utilisé'
            ' et ne peut pas être entièrement numérique')

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        instance = User.objects.filter(username=username)
        if instance.count():
            raise ValidationError(_("Nom d'utilisateur existe déjà"))
        return username

    def clean_email(self):
        email       = self.cleaned_data['email'].lower()
        instance    = User.objects.filter(email=email)
        if instance.count():
            raise ValidationError(_("Email existe déjà"))
        return email 

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if not password1 or not password2:
            raise ValidationError(_('Veuillez entrer un mot de passe valide'))

        if password1 and password2 and password1 != password2:
            raise ValidationError(_('Mots de passes ne sont pas identiques'))
        return password2 

    def save(self, commit=True):
        '''
            Surcharger la méthode save du formulaire et retourner
            :account: instance du modèle Account
            :user: instance de l'utilisateur crée
        '''
        # En cas de réussite: deux objets user et account seront crées     
        user = User.objects.create_user(
            username=self.cleaned_data['username'].lower(),
            email=self.cleaned_data['email'].lower(),
            last_name=self.cleaned_data['last_name'].lower(),
            first_name=self.cleaned_data['first_name'].lower(),
            password=self.cleaned_data['password2']
        )
        account             = account_models.Account.objects.get(user=user)
        account.birth_date  = self.cleaned_data['birth_date']
        account.info        = self.cleaned_data['info']
        return account, user
             

