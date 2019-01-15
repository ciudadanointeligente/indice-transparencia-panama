from django.shortcuts import render
from django.views.generic.edit import UpdateView
from extra_views import CreateWithInlinesView, UpdateWithInlinesView, InlineFormSetFactory
from django.views.generic.detail import DetailView
from indice_transparencia.models import Person, Contact
from indice_transparencia.forms import PersonForm
from django.template.response import TemplateResponse


class PersonUpdateView(UpdateWithInlinesView):
    model = Person
    form_class = PersonForm
    template_name = "update_candidate_info.html"

    def get_object(self, queryset=None):
        self.identifier = self.kwargs['identifier']
        self.person = Person.objects.get(contact__identifier=self.identifier)
        return self.person

    #def form_valid(self, form):
    #    form.save()
    #    return TemplateResponse(self.request, 'thanks_for_updating_info.html', {'person': self.person})

    def get_context_data(self, *args, **kwargs):
        context = super(PersonUpdateView, self).get_context_data(*args, **kwargs)
        context['contact'] = Contact.objects.get(identifier=self.identifier)
        return context

class CandidateProfileView(DetailView):
    model = Person
    template_name = "candidate_info.html"
