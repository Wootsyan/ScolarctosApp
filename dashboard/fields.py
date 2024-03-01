from django.forms import ModelChoiceField, ModelMultipleChoiceField

class SchoolChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.name} - ul. {obj.street}, {obj.postcode} {obj.city}'
    
class SchoolGuardianMultipleChoiceField(ModelMultipleChoiceField):
    def label_from_instance(self, obj):
        return ''
    
class TeamLeaderChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.first_name} {obj.last_name} ({obj.email})'