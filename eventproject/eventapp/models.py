from django.db import models

class User(models.Model):
    firstname = models.CharField(max_length=50,null=True,blank=True)
    lastname = models.CharField(max_length=50,null=True,blank=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=10,unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.email
    
