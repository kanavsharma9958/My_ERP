from django.urls import path
from . import views

urlpatterns = [
    path('check-status/', views.check_fee_status_view, name='check_fee_status'),
    path('generate-invoices/', views.generate_invoices_view, name='generate_invoices'),
    path('payment/<int:payment_id>/receipt/', views.payment_receipt_view, name='payment_receipt'),
    path('ajax/get-course-fee-details/<int:course_id>/', views.get_course_fee_details_view, name='get_course_fee_details'),
    
    # यह नया URL है
    path('reports/fee-collection/', views.fee_collection_report_view, name='fee_collection_report'),
]