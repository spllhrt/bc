from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from djongo import models  # Import djongo to use with MongoDB

# Custom manager to handle user creation
class UserManager(BaseUserManager):
    def create_user(self, email, fname, lname, password=None, **extra_fields):
        """
        Create and return a regular user with an email and password.
        """
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, fname=fname, lname=lname, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, fname, lname, password=None, **extra_fields):
        """
        Create and return a superuser with an email, password, and other necessary fields.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        
        return self.create_user(email, fname, lname, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    role = models.CharField(max_length=255, default='user')
    status = models.CharField(max_length=255, default='active')
    profile_picture = models.ImageField(upload_to='profile_pics/', default='../static/assets/img/icon.png')
    
    # Avoid using last_login field
    last_login = None  # Ensure it's not included

    # Adding the missing fields
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'lname']

    def __str__(self):
        return f"{self.fname} {self.lname}"



class Place(models.Model):
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=20, choices=[("barangay_hall", "Barangay Hall"), ("police_station", "Police Station")])
    address = models.TextField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    def __str__(self):
        return self.name

