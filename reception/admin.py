from django.contrib import admin
from .models import DocumentType, Notice

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_required')
    search_fields = ('name',)

# --- यह नया एडमिन रजिस्ट्रेशन जोड़ा गया है ---
@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'college', 'publish_date', 'is_active')
    list_filter = ('is_active', 'college')
    search_fields = ('title', 'content')
    list_editable = ('is_active',)