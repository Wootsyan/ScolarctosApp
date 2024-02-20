from django.urls import reverse_lazy
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import DetailView
from django.db.models.functions import Lower

from dashboard.models import School
from users.models import CustomUser
from dashboard.forms import SchoolsGuardianForm

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
class SchoolsGuardianListView(PermissionRequiredMixin, ListView):
    context_object_name = 'schools'
    template_name = 'dashboard/schools/guardian-list.html'

    def get_context_data(self, **kwargs):
        context = super(SchoolsGuardianListView, self).get_context_data(**kwargs)
        context['page_name'] = 'Moje szkoły'
        return context
    
    def get_queryset(self):    
        return self.request.user.guardians.all()
    
    def has_permission(self):
        if self.request.user.user_type == CustomUser.GUARDIAN:
            return True
        else:
            return False
    
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
        self.object = form.save()
        self.object.added_by = self.request.user
        if self.request.user.user_type in (CustomUser.ADMIN, CustomUser.ORGANIZER):
            self.object.accepted = True
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())
    
    def get_success_url(self):
        kwargs = {'pk': self.object.id}
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
    
    def form_valid(self, form):
        school = form.save()
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
class SchoolsGuardianUpdateView(PermissionRequiredMixin, FormView):
    context_object_name = 'schools'
    template_name = 'dashboard/schools/guardian-edit.html'
    form_class = SchoolsGuardianForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(SchoolsGuardianUpdateView, self).get_context_data(**kwargs)
        context['page_name'] = f"Edycja listy Twoich szkół"
        context['schools'] = School.objects.filter(accepted=True).order_by(Lower('name'))
        return context

    def has_permission(self):
        if self.request.user.user_type == CustomUser.GUARDIAN:
            return True
        else:
            return False
        
    def form_valid(self, form):
        # Check if removed school from list is not connected with guardian's team
        self.request.user.guardians.set(form.cleaned_data['schools'])
        self.request.user.save()
        return HttpResponseRedirect(self.get_success_url())
        
    def get_success_url(self):
        if '_save' in self.request.POST:
            return reverse_lazy('dashboard:schools-guardian-list')
        elif '_continue' in self.request.POST:
            return reverse_lazy('dashboard:schools-guardian-edit')

@method_decorator(login_required, name='dispatch')
class SchoolsDeleteView(PermissionRequiredMixin, DeleteView):
    model = School
    context_object_name = 'school'
    template_name = 'dashboard/schools/delete.html'
    permission_required = ('dashboard.delete_school')

    def get_context_data(self, **kwargs):
        context = super(SchoolsDeleteView, self).get_context_data(**kwargs)
        context['page_name'] = f"Szkoła: {context['school'].name}"
        return context
    
    def get_success_url(self):
        return reverse_lazy('dashboard:schools-list')