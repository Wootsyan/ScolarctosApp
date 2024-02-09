from django.forms import ModelChoiceField

class SchoolChoiceField(ModelChoiceField):
    def label_from_instance(self, obj):
        return f'{obj.name} - ul. {obj.street}, {obj.postcode} {obj.city}'