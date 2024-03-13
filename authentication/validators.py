from django.core.exceptions import ValidationError

def only_int_validator(value): 
    if value.isdigit() == False:
        raise ValidationError('Upewnij się, że ta wartość zawiera tylko cyfry.')
