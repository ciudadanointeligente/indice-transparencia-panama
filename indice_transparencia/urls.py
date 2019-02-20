from django.urls import path
from .views import PersonUpdateView, CandidateProfileView, RankingListView, IndexView
from django.views.generic.base import TemplateView

urlpatterns = [
    #path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('', IndexView.as_view(), name='index'),
    path('nosotros', TemplateView.as_view(template_name='about.html'), name='about'),
    path('info', TemplateView.as_view(template_name='info.html'), name='info'),
    path('about', TemplateView.as_view(template_name='about_index.html'), name='about_index'),
    path('actualizar_candidato/<str:identifier>/', PersonUpdateView.as_view(), name='update-person-data'),
    path('profile/<str:slug>/', CandidateProfileView.as_view(), name='candidate-profile'),
    path('ranking', RankingListView.as_view(), name='ranking'),
    # reverse('candidate-profile', kwargs={'slug': self.slug}) >> /profile/perrito-lindo
    # {% url 'candidate-profile' slug=person.slug %} >> /profile/perrito-lindo
    # {{ person.get_absolute_url }} >> /profile/perrito-lindo
]
