from django.urls import path, include
from .views import (LoginView, RefreshView, RegisterView, 
                    MeView, LogoutView, HasCreatedProfile, 
                    UserProfileView, VerifyEmail, PreVerEmail,
                    PreResetPassword, ResetPassword, )
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register("profile", UserProfileView)

urlpatterns = [
    path('', include(router.urls)),
    path('login', LoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('refresh', RefreshView.as_view()),
    path('me', MeView.as_view()),
    path('logout', LogoutView.as_view()),
    path('check-profile', HasCreatedProfile.as_view()),
    path('ver-email/<str:auth>', VerifyEmail.as_view()),
    path('pre-ver-email/<str:email>', PreVerEmail.as_view()),
    path('pre-reset-password', PreResetPassword.as_view()),
    path('reset-password/<str:auth>', ResetPassword.as_view()),
]