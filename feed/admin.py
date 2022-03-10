from django.contrib import admin
from .models import (
    Answers,
    FeedAnswersImage,
    FeedQuestionImage, 
    Question,
    FeedAnswerVideo,
    FeedQuestionVideo
)

admin.site.register((Answers, FeedAnswersImage, FeedQuestionImage, 
    Question, FeedAnswerVideo, FeedQuestionVideo, ))
