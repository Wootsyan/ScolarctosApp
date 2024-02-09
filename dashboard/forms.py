from django.forms import ModelForm
from django.db.models.functions import Lower

from dashboard.models import Team, School
from dashboard.fields import SchoolChoiceField

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
