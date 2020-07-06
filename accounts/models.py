from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin = False):
        if not email:
            raise ValueError("Users must have an email address")    # custom user using emails now
        if not password:
            raise ValueError("Password is required")
        user_obj = self.model(
            email = self.normalize_email(email)     # Django method
        )
        user_obj.set_password(password)     # Django also for changing pwd
        user_obj.staff  = is_staff
        user_obj.admin  = is_admin
        user_obj.active = is_active
        user_obj.save(using=self._db)   # saves into db
        return user_obj

    def create_staffuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True
        )
        return User

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return User



    # supercedes DJango user class
class User(AbstractBaseUser):
    email       = models.EmailField(unique=True, max_length=255, default="test@gmail.com")
    active      = models.BooleanField(default=True) # can login
    staff       = models.BooleanField(default=False) # regular user
    admin       = models.BooleanField(default=False) # super
    # timestamp   = models.DateTimeField(auto_now_add=True, default=timezone.now)
    # confirm   = models.BooleanField(default=False)
    # confirmed_date = models.DateTimeField(default=False)


    USERNAME_FIELD = "email"    #declare this the user name explicitly
    REQUIRED_FIELDS = []  # add any mandatory in the array ex ["staff"] unique to this class

    # user manager setup (vs Django default)
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active


# class Profile(models.Model):
  #  user = models.OneToOneField(User)

class GuestEmail(models.Model):
    email       = models.EmailField()
    active      = models.BooleanField(default=True)
    update      = models.DateTimeField(auto_now=True)
    timestamp   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email