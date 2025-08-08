from django.urls import path
from . import views

urlpatterns = [
    # यह हमारे 'Batch Invoice Generation' वाले पेज का रास्ता बनाएगा
    path('generate/', views.generate_invoices_view, name='generate_invoices'),
    path('check-status/', views.check_fee_status_view, name='check_fee_status'),
]