from django.conf import settings

def file_directory_path(instance, filename):
    if instance.id and instance.teams.exists():
        return f'{settings.STATIC_DOCUMENTS_DIR}teams/{instance.teams.first().id}/{filename}'
    
    return f'{settings.STATIC_DOCUMENTS_DIR}{filename}'
    

