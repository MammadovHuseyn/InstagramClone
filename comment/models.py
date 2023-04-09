from django.db import models
from core.models import Posts , CustomUser
# Create your models here.

class Comment(models.Model):
    post = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.body
    