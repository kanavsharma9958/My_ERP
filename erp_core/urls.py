from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    # Admin Panel URL
    path('admin/', admin.site.urls),
    
    # App URLs
    path('admissions/', include('admissions.urls')),
    path('fees/', include('fees.urls')),
    path('academics/', include('academics.urls')),
    path('examinations/', include('examinations.urls')),
    
    # Login/Logout URLs
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

# This is to make media files (like logos) work during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)