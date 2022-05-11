from django.db import models

from django.contrib.auth.models import User

class Users(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    user_type=models.CharField(
                               max_length=10,
                               choices=[('Admin','Admin'),('Shopuser','Shopuser'),('Customer','Customer')]
                               )

    def __str__(self):
        return self.user.username