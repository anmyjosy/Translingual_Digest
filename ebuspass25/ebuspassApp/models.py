from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    usertype = models.CharField(max_length = 20)
    pswrd = models.CharField(max_length = 30,null=True)

class UserReg(models.Model):
    usr_con = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=20)
    email = models.EmailField(max_length=20)
    Address = models.CharField(max_length=200,null = True)




