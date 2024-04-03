from django.db import models
from datetime import date,timezone

from accounts.models import *
class appointment(models.Model):
    patient_id=models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    patient_name = models.CharField(max_length=255 , default='unknown user')
    datetime = models.DateTimeField(auto_now_add=False,null=True)
    appointment_state = models.CharField(max_length=255) #accept reject etcccccc
    note = models.TextField()
    rejection_reason = models.TextField(blank=True, null=True)


class schedule(models.Model):
    doctor_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    date = models.DateField()
    starttime = models.TimeField()
    endtime = models.TimeField()



class prescription(models.Model):
    appointment_id=models.ForeignKey(appointment,on_delete=models.CASCADE, default=None)
    date = models.DateField()
    duration = models.IntegerField( default=0)
    age = models.IntegerField()
    gender = models.CharField(max_length=20 , default='rather not say')

class medicine(models.Model):
    medicine_name = models.CharField(max_length=100)
    price = models.IntegerField(null=True) #per medicine

class prescribedMedicine(models.Model):
    prescription_id=models.ForeignKey(prescription,on_delete=models.CASCADE, default=None)
    medicine_id=models.ForeignKey(medicine,on_delete=models.CASCADE)
    dosage=models.CharField(max_length=10)
    quantity=models.IntegerField()



class bill(models.Model):
    appointment_id=models.ForeignKey(appointment,on_delete=models.CASCADE, default=None)
    date = models.DateField(default=None)
    final_amount = models.IntegerField()

class billmed(models.Model):
    bill_id=models.ForeignKey(bill,on_delete=models.CASCADE, default=None)
    medicine_id=models.ForeignKey(medicine,on_delete=models.CASCADE)
    

class timeslot(models.Model):
    doctor_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    slot_date = models.DateField()
    is_available = models.CharField(max_length=12, default='available')
    starttime = models.TimeField()





class feedback(models.Model):
    patient_id=models.ForeignKey(Patient,on_delete=models.CASCADE)
    doctor_id=models.ForeignKey(Doctor,on_delete=models.CASCADE)
    comment = models.TextField()
