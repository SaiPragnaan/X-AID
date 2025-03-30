from django.db import models
from django.contrib.auth.models import User

# Create your models here.

def user_image_path(instance, filename):
    return f"uploads/user_{instance.user.id}/{filename}"

def bot_image_path(instance, filename):
    return f"uploads/bot/{filename}"

class Chat(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    message=models.TextField()
    response=models.TextField()
    image = models.ImageField(upload_to=user_image_path, blank=True, null=True, default="default/user_placeholder.png")
    bot_image = models.ImageField(upload_to=bot_image_path, blank=True, null=True, default="default/bot_placeholder.png")
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.message}'