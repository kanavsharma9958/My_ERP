from django.urls import path
from . import views

urlpatterns = [
    path('apply/', views.admission_form_view, name='admission_form'),
    path('success/', views.success_view, name='admission_success'),
    path('student/<str:roll_number>/id-card/', views.id_card_view, name='id_card_view'),
    
    path('ajax/get-required-documents/<int:course_id>/', views.get_required_documents_view, name='get_required_documents'),
    path('ajax/get-subjects-for-course/<int:course_id>/', views.get_subjects_for_course_view, name='get_subjects_for_course'),
    path('ajax/get-courses-for-college/<int:college_id>/', views.get_courses_for_college_view, name='get_courses_for_college'),
    
    # यह नया URL है
    path('ajax/get-semesters-for-course/<int:course_id>/', views.get_semesters_for_course_view, name='get_semesters_for_course'),
]