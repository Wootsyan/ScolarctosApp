from django import forms
from users.forms import CustomUserCreationForm
from users.models import CustomUser
from django.utils.translation import gettext_lazy as _

class RegisterForm(CustomUserCreationForm):
    SELECTED_USER_TYPE_CHOICES = (
        CustomUser.USER_TYPE_CHOICES[CustomUser.STUDENT-1],
        CustomUser.USER_TYPE_CHOICES[CustomUser.GUARDIAN-1],
    )
    user_type = forms.ChoiceField(choices=SELECTED_USER_TYPE_CHOICES)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['user_type'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'user_type')

class LoginForm(forms.Form):
    email = forms.EmailField(label=_("Email"), max_length=254)
    password = forms.CharField(label=_("Password"), widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ('email', 'password',)