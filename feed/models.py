from django.db import models


class FeedQuestionImage(models.Model):
    image = models.ImageField(upload_to="questions")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.image)} || {self.created_at}"


        

class FeedAnswersImage(models.Model):
    image = models.ImageField(upload_to="answers")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{str(self.image)} || {self.created_at}"


        

class FeedAnswerVideo(models.Model):
    video = models.FileField(upload_to="answer_video")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  f"{str(self.video)} || {self.created_at}"



class FeedQuestionVideo(models.Model):
    video = models.FileField(upload_to="question_video")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  f"{str(self.video)} || {self.created_at}"


class Question(models.Model):
    user = models.ForeignKey('user_controller.UserProfile', related_name="question_author", on_delete=models.CASCADE)
    question_image = models.ManyToManyField(FeedQuestionImage, related_name="feed_question_image")
    question_video = models.ForeignKey(FeedQuestionVideo, null=True, on_delete=models.SET_NULL, related_name="feed_question_video")
    question_category = models.ManyToManyField("user_controller.CategoryOfInterest", related_name="feed_question_category")
    question_text = models.TextField()
    reaction = models.ManyToManyField('user_controller.UserProfile', related_name="feed_question_reaction")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user} | {self.question_category} | {self.question_text[:50]}"



class Answers(models.Model):
    user = models.ForeignKey('user_controller.UserProfile', related_name="question_answer_author", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name="answers_to_questions", on_delete=models.CASCADE) #The answer field would be delete when the question is deleted
    answer_text = models.TextField()
    answer_image = models.ManyToManyField(FeedAnswersImage, related_name="feed_answer_img")
    answer_video = models.ForeignKey(FeedAnswerVideo, null=True, on_delete=models.SET_NULL, related_name="feed_answer_video")
    reaction = models.ManyToManyField('user_controller.UserProfile', related_name="feed_answer_reaction")
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} | {self.answer_text[:50]}"








