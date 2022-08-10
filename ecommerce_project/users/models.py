"""
    user models module
"""

from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):

    """
        user manager
    """

    def create_user(self, email,user_type, password = None):

        """
            create user
        """

        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            user_type=user_type,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, user_type, password=None):

        """
            create super user
        """

        user = self.create_user(
            email,
            password=password,
           user_type=user_type,
        )

        user.is_admin = True
        user.save(using=self._db)

        return user

class MyUser(AbstractBaseUser):

    """
        custom  user model
    """

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(max_length = 20, default = '')
    dob = models.DateField(default = timezone.now, blank = True)
    gender = models.CharField(max_length = 10, default='', blank = True)
    adress = models.TextField(default='', blank = True)
    shop_name = models.CharField(max_length=100, blank = True, default='')
    shop_type = models.CharField(max_length=100, blank = True, default='')

    user_type=models.CharField(
                               max_length=10,
                               choices=[('1','Admin'),('2','Shopuser'),('3','Customer')]
                               )

    objects = MyUserManager()

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


    USERNAME_FIELD = 'email'
  