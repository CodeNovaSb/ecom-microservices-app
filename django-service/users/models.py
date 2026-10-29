from django.conf import settings
from django.db import models

# Create your models here.
class Users(models.Model):

    name = models.CharField(max_length=100)
    mail = models.EmailField(max_length=100)
    address = models.CharField(max_length=200)
    phone_no = models.CharField(max_length=15)

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.name
