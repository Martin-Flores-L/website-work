from django.db import models

# Create your models here.
class Record(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return (f"{self.name} - {self.phone} - {self.email} - {self.address} - {self.date_created}")