from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admissions/', include('admissions.urls')),
    path('fees/', include('fees.urls')),
    path('faculty/', include('academics.urls')),
    
    # --- यह लाइन होम पेज के लिए ज़रूरी है ---
    path('', include('core.urls')), 
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)