from django.shortcuts import render
from django.views.generic.edit import UpdateView
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from indice_transparencia.models import (Person, Contact, EducationalRecord,
                                         WorkRecord, JudiciaryProcessRecord,
                                         update_mark_and_position_in_ranking)
from indice_transparencia.forms import PersonForm
from indice_transparencia.filters import PersonFilter
from django.template.response import TemplateResponse
from django.views.generic.base import TemplateView
from django import forms
from django.conf import settings
from django.core.cache import cache

class EducationalRecordInline(InlineFormSetFactory):
    model = EducationalRecord
    fields = ['name', 'institution', 'start', 'end']
    factory_kwargs = {'extra': 1}


class WorkRecordInline(InlineFormSetFactory):
    model = WorkRecord
    fields = ['name', 'institution', 'start', 'end']
    factory_kwargs = {'extra': 1}


class JudiciaryRecordInline(InlineFormSetFactory):
    model = JudiciaryProcessRecord
    fields = ['number', 'date', 'kind', 'result']
    factory_kwargs = {'extra': 1}
    # formset_kwargs = {'widgets' : {'date': forms.DateInput(attrs={'class':'datepicker'})}}



class PersonUpdateView(UpdateWithInlinesView):
    model = Person
    form_class = PersonForm
    template_name = "update_candidate_info.html"
    inlines = [EducationalRecordInline, WorkRecordInline, JudiciaryRecordInline]

    def get_object(self, queryset=None):
        self.identifier = self.kwargs['identifier']
        self.person = Person.objects.get(contact__identifier=self.identifier)
        return self.person

    def forms_valid(self, form, inlines):
        '''
        Jordito querido mi corazón
        acá se recalcula el ranking y la mark cuando un candidato responde el formulario
        '''
        response = super(PersonUpdateView, self).forms_valid(form, inlines)
        update_mark_and_position_in_ranking(self.object)
        return response

    def get_context_data(self, *args, **kwargs):
        context = super(PersonUpdateView, self).get_context_data(*args, **kwargs)
        context['contact'] = Contact.objects.get(identifier=self.identifier)
        return context


class UnderDevelopmentMixin(object):
    def get_template_names(self):
        if settings.SHOW_UNDER_DEVELOPMENT_TEMPLATE:
            return ['working.html']
        return super().get_template_names()


class CandidateProfileView(UnderDevelopmentMixin, DetailView):
    model = Person
    template_name = "candidate_info.html"


class RankingListView(UnderDevelopmentMixin, ListView):
    model = Person
    template_name = 'ranking.html'
    context_object_name = "persons"
    
    def get_queryset(self):
        qs = super().get_queryset().order_by('position_in_ranking')
        return qs
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PersonFilter(self.request.GET, queryset=self.get_queryset().order_by('position_in_ranking'))
        return context
    
class IndexView(UnderDevelopmentMixin, TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        persons_index_cache_key = 'persons_index'
        if cache.get(persons_index_cache_key):

            persons = cache.get('persons_index')
            
        else:
            persons = Person.objects.order_by('position_in_ranking')[:10]

            cache.set(persons_index_cache_key, persons, 300)
        context['persons'] = persons
        context['debug'] = settings.DEBUG
        return context    
    