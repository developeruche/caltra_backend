# @developeruche
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

# ======================================================
    # This is are UTIL models
# ======================================================
class ProfileImage(models.Model):
    image = models.FileField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.image)} || {self.created_at}"


class CategoryOfInterest(models.Model):
    name = models.CharField(max_length=122)

    def __str__(self):
        return f"{self.name}"


class Campus(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

GENDER_CHOICES = (
    ('Male', 'male', ),
    ('Female', 'female', ),
)


# =====================================================


# Creating the Base(foundation) of the user{BaseManager}
class CustomUserManager(BaseUserManager): #Inheriting form the django BaseUSerManager
    def _create_user(self, username, password, **extra_fields):
        if not username: #condition is true when the username is not provided
            raise ValueError("Username field is required")

        user = self.model(username=username, **extra_fields)
        user.set_password(password) #This method would hash the password before storing it
        user.save()

        return user


    def create_superuser(self, username,password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(username, password, **extra_fields)

    def update_password(self, email, password):
        if not password:
            raise ValueError(
                "The password Field is required for this operation.")
        user = self.model.objects.get(email=email)
        # Setting the password in a way that it would be hashed
        user.set_password(password)
        user.save()




class CustomUser(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(unique=True, max_length=100)
    email = models.EmailField(unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_ver_email = models.BooleanField(default=False)
    is_disabled = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) #This is going to be used to kickout people for the network
    is_online = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = "username"
    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        ordering = ("created_at",)


class UserProfile(models.Model):
    user = models.OneToOneField(
        CustomUser, related_name="user_profile", on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(choices=GENDER_CHOICES, max_length=20)
    campus = models.ForeignKey(Campus, related_name="user_campus", null=True, on_delete=models.SET_NULL)
    country_code = models.CharField(max_length=4, default='+234')
    tel_number = models.PositiveIntegerField(null=True)
    caption = models.CharField(max_length=250)
    about = models.TextField()
    profile_picture = models.ForeignKey(
        ProfileImage, related_name="user_image", on_delete=models.SET_NULL, null=True)
    interest = models.ManyToManyField(CategoryOfInterest, related_name="user_interest")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    followers = models.ManyToManyField(CustomUser, related_name="user_followers", null=True)
    
    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ("created_at",)


# This would be responsible for the authentication of the user
class Jwt(models.Model):
    user = models.OneToOneField(
        CustomUser, related_name="login_user", on_delete=models.CASCADE)
    access = models.TextField()
    refresh = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)