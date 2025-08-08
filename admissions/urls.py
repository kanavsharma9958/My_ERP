from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.admission_form_view, name='admission_apply'),
path('success/', views.success_view, name='admission_success'),
 path('student/<str:roll_number>/id-card/', views.id_card_view, name='id_card_view'),
]
