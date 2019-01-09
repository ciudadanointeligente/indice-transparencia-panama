from django.urls import path
from .views import PersonUpdateView
from django.views.generic.base import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('actualizar_candidato/<str:identifier>/', PersonUpdateView.as_view(), name='update-person-data'),
]