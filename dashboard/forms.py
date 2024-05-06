from django.forms import Form, ModelForm, CheckboxSelectMultiple, Select, BooleanField, ChoiceField
from django.db.models.functions import Lower
from django.core.validators import FileExtensionValidator 

from dashboard.models import Team, School
from dashboard.fields import SchoolChoiceField, SchoolGuardianMultipleChoiceField, TeamLeaderChoiceField
from users.models import CustomUser
from files.models import File

class CreateTeamForm(ModelForm):
    school = SchoolChoiceField(queryset=School.objects.filter(accepted=True).order_by(Lower('name')))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name in self.fields:
            if field_name == 'editable':
                self.fields[field_name].widget.attrs['class'] = 'custom-control-input'
            else:
                self.fields[field_name].widget.attrs['class'] = 'form-control'


    class Meta:
        model = Team
        fields = [ 
            'name', 
            'school',
            'description',
            'editable'
        ]

class UpdateTeamForm(CreateTeamForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.instance.team_guardian:
            self.fields['school'].disabled = True
            GUARDIAN_CHOICES = (
                (0, f'{self.instance.team_guardian.guardian.first_name} {self.instance.team_guardian.guardian.last_name}'),
                (1, 'Brak'),
            )

            self.fields['guardian'] = ChoiceField(choices=GUARDIAN_CHOICES)
            self.fields['guardian'].widget.attrs['class'] = 'form-control'



class CreateTeamMemberForm(ModelForm):
    gdpr_consent = BooleanField(required=False)
    parental_consent = BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name in ['first_name', 'last_name']:
            self.fields[field_name].widget.attrs['class'] = 'form-control'
        
        for field_name in ['gdpr_consent', 'parental_consent']:
            self.fields[field_name].widget.attrs['class'] = 'custom-control-input'
    
    class Meta:
        model = CustomUser
        fields = [ 
            'first_name', 
            'last_name',
        ]

class UpdateTeamMemberForm(CreateTeamMemberForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.initial['gdpr_consent'] = self.instance.gdpr.gdpr_consent
        self.initial['parental_consent'] = self.instance.gdpr.parental_consent

class UpdateTeamLeaderForm(UpdateTeamMemberForm):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        for field_name in ['first_name', 'last_name']:
            self.fields[field_name].disabled = True

class ConnectTeamLeaderForm(ModelForm):
    leader = TeamLeaderChoiceField(
        queryset=CustomUser.objects.filter(is_active=True, user_type=CustomUser.STUDENT, team__isnull=True),
        widget=Select,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['leader'].widget.attrs['class'] = 'form-control'

    class Meta:
        model = Team
        fields = [ 
            'leader',
        ]

class SchoolsGuardianForm(Form):
    schools = SchoolGuardianMultipleChoiceField(
        queryset=None,
        widget=CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        self.fields['schools'].queryset = School.objects.filter(accepted=True).order_by(Lower('name'))
        self.initial['schools'] = self.request.user.schools.all()

class TeamsAddFile(ModelForm):
    valid_extensions = [
        'PDF', 
        'JPG',
        'PNG',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['path'].widget.attrs['class'] = 'custom-file-input'
        self.fields['path'].validators = [FileExtensionValidator(self.valid_extensions)]

    class Meta:
        model = File
        fields = [ 
            'path',
        ]