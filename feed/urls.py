from django.urls import path, include
from .views import (QuestionView, AnswerView)
from rest_framework.routers import DefaultRouter

router = DefaultRouter(trailing_slash=False)

router.register("question", QuestionView)
router.register("answer", AnswerView)

urlpatterns = [
    path('', include(router.urls)),
]