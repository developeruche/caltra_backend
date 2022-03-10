from django.contrib import admin
from .models import (CustomUser, CategoryOfInterest, 
UserProfile, Jwt, ProfileImage, Campus)


admin.site.register((CustomUser, CategoryOfInterest, UserProfile, Jwt, ProfileImage, Campus, ))
