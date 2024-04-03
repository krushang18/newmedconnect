from django.contrib.auth.models import AbstractBaseUser, BaseUserManager ,PermissionsMixin
from django.db import models

class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)

class CustomUserManager(BaseUserManager):
    def create_user(self, email,first_name, password=None):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            first_name=first_name
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email,first_name, password=None):
        user = self.create_user(
            email = self.normalize_email(email),
            password = password,
            first_name = first_name
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self.db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=15)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)
    type = models.CharField(max_length=16, default='patient')
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name']

    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None): 
        return self.is_admin
    def has_module_perms (self, app_label): 
        return True
    
class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    doctor_addr = models.ForeignKey(Address, on_delete=models.CASCADE)

    qualification = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    certificate_no = models.CharField(max_length=255)
    fees = models.IntegerField()
    profile_img = models.ImageField(upload_to="doctors_profile_images", default='doctors_profile_images/default.png')

    def __str__(self):
        return self.user.email

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    patient_addr = models.ForeignKey(Address, on_delete=models.CASCADE)

    date_of_birth = models.DateField()
    blood_group = models.CharField(max_length=5)
    profile_img = models.ImageField(upload_to="patient_profile_images", default='patient_profile_images/default.png')

    def __str__(self):
        return self.user.email
    
# class Notifications(models.Model):
#     user=models.ForeignKey(Patient, on_delete=models.CASCADE)
#     message=models.TextField(max_length=250)