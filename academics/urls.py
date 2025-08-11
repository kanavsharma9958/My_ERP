from django.urls import path
from . import views
from django.contrib.auth import views as auth_views # Django के बने-बनाए व्यूज

urlpatterns = [
    # Authentication URLs
    path('login/', views.faculty_login_view, name='faculty_login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='faculty_logout'),

    # Dashboard and other views
    path('dashboard/', views.faculty_dashboard_view, name='faculty_dashboard'),
    path('attendance/mark/<int:schedule_id>/', views.mark_attendance_view, name='mark_attendance'),
    path('marks/select/', views.select_test_for_marks_view, name='select_test_for_marks'),
    path('marks/entry/<int:unit_test_id>/<int:subject_id>/', views.enter_marks_view, name='enter_marks'),
]