from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager
)

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, first_name=None, password=None, is_active=True, is_staff=False, is_admin = False):
        if not email:
            raise ValueError("Users must have an email address")    # custom user using emails now
        if not password:
            raise ValueError("Password is required")
            # if not first_name:            -- only if I want to use name as mandatory
                #  raise ValueError("Need to enter a name")
        user_obj = self.model(
            email = self.normalize_email(email),     # Django method
            first_name = first_name
        )
        user_obj.set_password(password)     # Django also for changing pwd
        user_obj.staff  = is_staff
        user_obj.admin  = is_admin
        user_obj.active = is_active
        user_obj.first_name = first_name
        user_obj.save(using=self._db)   # saves into db
        return user_obj

    def create_staffuser(self, email, first_name=None, password=None):
        user = self.create_user(
            email,
            first_name=first_name,
            password=password,
            is_staff=True
        )
        return User

    def create_superuser(self, email, first_name=None, password=None):
        user = self.create_user(
            email,
            first_name=first_name,
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
    timestamp   = models.DateTimeField(auto_now_add=True)
    verified    = models.BooleanField(default=False)    # email is confirmed valid and authenticated
    first_name  = models.CharField(max_length=50, blank=True, null=True)
    # confirm   = models.BooleanField(default=False)
    # confirmed_date = models.DateTimeField(default=False)

        # declare this the user name explicitly
    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []  # add any mandatory in the array ex ["staff"] unique to this class

        # user manager setup (vs Django default)
    objects = UserManager()

    def __str__(self):
        return self.email

    def get_first_name(self):
        if self.first_name:
            return self.first_name
        return self.email

    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

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