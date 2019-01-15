from django.urls import path
from .views import PersonUpdateView, CandidateProfileView
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('actualizar_candidato/<str:identifier>/', PersonUpdateView.as_view(), name='update-person-data'),
    path('profile/<str:slug>/', CandidateProfileView.as_view(), name='candidate-profile'),
    # reverse('candidate-profile', kwargs={'slug': self.slug}) >> /profile/perrito-lindo
    # {% url 'candidate-profile' slug=person.slug %} >> /profile/perrito-lindo
    # {{ person.get_absolute_url }} >> /profile/perrito-lindo
]
