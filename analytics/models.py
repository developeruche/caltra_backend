from django.db import models

class ActiveUser(models.Model):
    user = models.ManyToManyField('user_controller.CustomUser', related_name="active_user")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Active users for {self.created_at}"