from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.base import TemplateView

'''
### Main Views
'''
@method_decorator(login_required, name='dispatch')
class  IndexView(TemplateView):
        template_name = "dashboard/index.html"

'''
### Others Views
'''
def error_403(request, exception):
        return render(request, 'dashboard/errors/403.html')
