from django.db import models
from django.utils import timezone

class DocumentType(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Document Name")
    is_required = models.BooleanField(default=True, verbose_name="Is this document mandatory?")

    def __str__(self):
        return self.name

# --- यह नया मॉडल जोड़ा गया है ---
class Notice(models.Model):
    college = models.ForeignKey('core.College', on_delete=models.CASCADE, null=True, blank=True, help_text="Select a college to make this notice college-specific. Leave blank for a general notice.")
    title = models.CharField(max_length=200)
    content = models.TextField()
    publish_date = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True, help_text="Only active notices will be shown on the website.")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-publish_date']