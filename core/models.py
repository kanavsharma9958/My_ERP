from django.db import models

class College(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="College Name")
    code = models.CharField(max_length=10, unique=True, verbose_name="College Code (e.g., DC, LAW)")
    logo = models.ImageField(upload_to='college_logos/', verbose_name="College Logo", null=True, blank=True)
    address = models.TextField(verbose_name="Address", null=True, blank=True)
    contact_number = models.CharField(max_length=20, verbose_name="Contact Number", null=True, blank=True)

    def __str__(self):
        return self.name