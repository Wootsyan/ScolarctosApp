from django.forms import Form, ModelForm, ModelMultipleChoiceField, CheckboxSelectMultiple
from django.db.models.functions import Lower

from dashboard.models import Team, School
from dashboard.fields import SchoolChoiceField, SchoolGuardianMultipleChoiceField
from users.models import CustomUser

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

class SchoolsGuardianForm(Form):
    schools = SchoolGuardianMultipleChoiceField(
        queryset=None,
        widget=CheckboxSelectMultiple,
    )

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

        self.fields['schools'].queryset = School.objects.filter(accepted=True).order_by(Lower('name'))
        self.initial['schools'] = self.request.user.guardians.all()
