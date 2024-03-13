from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from users.forms import CustomUserCreationForm
from users.models import CustomUser
from .validators import only_int_validator


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

    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive."),
    }

    def __init__(self, request, *args, **kwargs):
        self.request = request
        super().__init__(*args, **kwargs)

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        self.user = authenticate(self.request, username=email, password=password)

        if self.user is None:
            raise self.get_invalid_login_error()
        else:
            self.confirm_login_allowed(self.user)

        return self.cleaned_data
    
    def get_user(self):
        return self.user
        
    def get_invalid_login_error(self):
        return ValidationError(
            self.error_messages["invalid_login"],
            code="invalid_login",
            params={"username": 'email'},
        )
    
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages["inactive"],
                code="inactive",
            )


class ConfirmationForm(forms.Form):
    confirm_code = forms.CharField(label="Confirmation Code", validators=[MinLengthValidator(6), MaxLengthValidator(6), only_int_validator])
    confirm_code.widget.attrs.update({'class': 'form-control text-center'})