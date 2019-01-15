from django.shortcuts import render
from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from indice_transparencia.models import Person, Contact, EducationalRecord
from indice_transparencia.forms import PersonForm, EducationalRecordInlineFormset
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
        educational_formset = EducationalRecordInlineFormset(
            self.request.POST,
            queryset=self.person.educational_records.all()
        )
        if educational_formset.is_valid():
            person = form.save()
            for edu_form in educational_formset:
                educational_record = edu_form.save(commit=False)
                educational_record.person = person
                educational_record.save()
            return TemplateResponse(self.request, 'thanks_for_updating_info.html', {'person': self.person})
        
        print("formset")
        print(educational_formset.as_table())
        print("Errores")
        print(educational_formset.errors)
        return self.form_invalid(form)
            

    def get_context_data(self, *args, **kwargs):
        context = super(PersonUpdateView, self).get_context_data(*args, **kwargs)
        context['contact'] = Contact.objects.get(identifier=self.identifier)
        context['formset'] = EducationalRecordInlineFormset(
            queryset=self.person.educational_records.all()
        )
        return context

class CandidateProfileView(DetailView):
    model = Person
    template_name = "candidate_info.html"
