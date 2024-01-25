from django.urls import reverse_lazy
from django.http import HttpResponseNotFound
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView

from dashboard.models import School
from users.models import CustomUser

'''
### Schools Views
'''

@method_decorator(login_required, name='dispatch')
class SchoolsListView(PermissionRequiredMixin, ListView):
    model = School
    context_object_name = 'schools'
    template_name = 'dashboard/schools/list.html'
    permission_required = ('dashboard.view_school')

    def get_context_data(self, **kwargs):
        context = super(SchoolsListView, self).get_context_data(**kwargs)
        context['page_name'] = 'Szkoły'
        if "type" in self.kwargs:
            context['school_type'] = self.kwargs["type"]
            if context['school_type'] == 1:
                context['page_name'] += ' podstawowe'
            elif context['school_type'] == 2:
                context['page_name'] += ' ponadpodstawowe'
        return context
    
    def get_queryset(self):
        if "type" in self.kwargs:
            school_type = self.kwargs["type"]

            if school_type not in (School.FIRST_LEVEL, School.SECOND_LEVEL):
                return HttpResponseNotFound
            
            return School.objects.filter(school_type=school_type)
        
        return School.objects.all()
    
@method_decorator(login_required, name='dispatch')
class SchoolsDetailView(PermissionRequiredMixin, DetailView):
    model = School
    context_object_name = 'school'
    template_name = 'dashboard/schools/detail.html'
    permission_required = ('dashboard.view_school')

    def get_context_data(self, **kwargs):
        context = super(SchoolsDetailView, self).get_context_data(**kwargs)
        context['page_name'] = f"{context['school'].name}"
        return context
    
@method_decorator(login_required, name='dispatch')
class SchoolsCreateView(PermissionRequiredMixin, CreateView):
    model = School
    template_name = 'dashboard/schools/add.html'
    permission_required = ('dashboard.add_school')

    fields = [ 
        'name', 
        'street',
        'postcode',
        'city',
        'school_type',
    ]

    def get_context_data(self, **kwargs):
        context = super(SchoolsCreateView, self).get_context_data(**kwargs)
        context['page_name'] = "Dodaj nową szkołę"
        for field in self.fields:
            context['form'].fields[field].widget.attrs['class'] = 'form-control'
        context['form'].fields['postcode'].widget.attrs['pattern'] = '[0-9]{2}-[0-9]{3}'
        context['form'].fields['postcode'].widget.attrs['placeholder'] = '12-345'
        return context
    
    def form_valid(self, form):
        school = form.save()
        school.added_by = self.request.user
        if self.request.user.user_type in (CustomUser.ADMIN, CustomUser.ORGANIZER):
            school.accepted = True
        school.save()
        return super().form_valid(form)
    
    def get_success_url(self):
        context_school = self.get_object()
        kwargs = {'pk': context_school.id}
        if '_save' in self.request.POST:
            return reverse_lazy('dashboard:schools-detail', kwargs=kwargs)
        elif '_continue' in self.request.POST:
            return reverse_lazy('dashboard:schools-edit', kwargs=kwargs)

@method_decorator(login_required, name='dispatch')
class SchoolsUpdateView(PermissionRequiredMixin, UpdateView):
    model = School
    context_object_name = 'school'
    template_name = 'dashboard/schools/edit.html'

    fields = [ 
        'name', 
        'street',
        'postcode',
        'city',
        'school_type',
        'accepted',
    ]

    def get_context_data(self, **kwargs):
        context = super(SchoolsUpdateView, self).get_context_data(**kwargs)
        context['page_name'] = f"Edycja: {context['school'].name}"
        for field in self.fields:
            context['form'].fields[field].widget.attrs['class'] = 'form-control'
        context['form'].fields['postcode'].widget.attrs['pattern'] = '[0-9]{2}-[0-9]{3}'
        context['form'].fields['postcode'].widget.attrs['placeholder'] = '12-345'
        return context

    def has_permission(self):
        context_school = self.get_object()
        if self.request.user == context_school.added_by:
            return True
        else:
            return self.request.user.has_perm('dashboard.change_school')
        
    def get_success_url(self):
        context_school = self.get_object()
        kwargs = {'pk': context_school.id}
        if '_save' in self.request.POST:
            return reverse_lazy('dashboard:schools-detail', kwargs=kwargs)
        elif '_continue' in self.request.POST:
            return reverse_lazy('dashboard:schools-edit', kwargs=kwargs)
