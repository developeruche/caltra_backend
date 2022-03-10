# from django.urls import path, include
from .views import (ActiveUser, )


urlpatterns = [
    path('activeusers', ActiveUser.as_view()),
]