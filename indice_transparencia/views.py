from django.shortcuts import render
from django.views.generic.edit import UpdateView
from indice_transparencia.models import Person, Contact
from indice_transparencia.forms import PersonForm
from django.template.response import TemplateResponse


class PersonUpdateView(UpdateView):
    model = Person
    form_class = PersonForm
    template_name = "update_candidate_info.html"

    def get_object(self, queryset=None):
        self.identifier = self.kwargs['identifier']
        self.person = Person.objects.get(contact__identifier=self.identifier)
        return self.person

    def form_valid(self, form):
        form.save()
        return TemplateResponse(self.request, 'thanks_for_updating_info.html', {'person': self.person})