from django.db import models
from accounts.models import Patient
# Create your models here.
class contact_us(models.Model):
    name=models.CharField(max_length=50)
    email= models.EmailField(max_length=254)
    subject=models.CharField(max_length=255)
    message=models.TextField()

class Notifications(models.Model):
    user=models.ForeignKey(Patient, on_delete=models.CASCADE)
    message=models.TextField(max_length=250)