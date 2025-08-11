from django.db import models

class College(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="College Name")
    code = models.CharField(max_length=20, unique=True, verbose_name="College Code")

    # --- यह नए फील्ड्स हैं ---
    logo = models.ImageField(upload_to='college_logos/', null=True, blank=True, verbose_name="College Logo")
    address = models.TextField(null=True, blank=True, verbose_name="Address")
    contact_number = models.CharField(max_length=20, null=True, blank=True, verbose_name="Contact Number")
    email = models.EmailField(null=True, blank=True, verbose_name="Email Address")

    def __str__(self):
        return self.name