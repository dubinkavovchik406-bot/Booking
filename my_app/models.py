from django.db import models

# Create your models here.
class Customer(models.Model):
    name = models.CharField(max_length=256)
    surname = models.CharField(max_length=256)
    email = models.EmailField()

    def __str__(self):
        return f"Customer {self.name} {self.surname}"

    class Meta:
        verbose_name = "Customer"
        verbose_name_plural = "Customers"
        ordering = ["name"]

