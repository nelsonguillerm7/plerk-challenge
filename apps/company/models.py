# Django
from django.db import models


class Company(models.Model):
    """Model the company"""

    name = models.CharField(max_length=256, verbose_name="Name")
    state = models.BooleanField(verbose_name="Status", default=True)

    class Meta:
        """Class information"""

        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name}"
