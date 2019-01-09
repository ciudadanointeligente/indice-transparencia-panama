from django.urls import path
from .views import PersonUpdateView
from django.views.generic.base import TemplateView

urlpatterns = [
    path('actualizar_candidato/<str:identifier>/', PersonUpdateView.as_view(), name='update-person-data'),
]