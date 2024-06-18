from django.db import models
import random

from django.contrib.auth.models import AbstractUser, BaseUserManager,AbstractBaseUser

class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        # Create and return a regular user with email and username
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        # Create and return a superuser with email, username, and password
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user




class User(AbstractBaseUser):
    USER_CHOICES = ((0, "Admin"), (1, "Organisation"))
   

    user_type = models.IntegerField(choices=USER_CHOICES, default=1)
    email = models.EmailField(unique=True)
   
   
 
   
   
    profile_image = models.CharField(max_length=255, blank=True, null=True) 
    username=models.CharField(max_length=255,unique=True,blank=True,null=True)

    objects = CustomUserManager()

   
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []
    # Add other required fields for creating a user
    class Meta:
        db_table = "users"
    def __str__(self):
        return self.email

    def json_object(self):
        return {
            "name": self.username,
            "email": self.email,
        }
    

class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    liked_by = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    def __str__(self):
        return self.title
    

class ImageUpload(models.Model):
    title = models.CharField(max_length=100)
    image = models.ImageField(upload_to='uploads/')

    def __str__(self):
        return self.title
