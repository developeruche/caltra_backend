from django.contrib import admin

from .models import (
    ActiveUser
)

admin.site.register((ActiveUser,  ))


