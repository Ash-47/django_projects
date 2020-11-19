from django.contrib.auth.models import AbstractUser
from django.db import models




class User(AbstractUser):
    following=models.ManyToManyField("self",symmetrical=False,default=0)
    liked_post=models.ManyToManyField("Post",related_name="liked_by",default=None,symmetrical=False,blank=True)
    followers=models.ManyToManyField("self",default='',related_name="follow",blank=True,symmetrical=False)

    def __str__(self):
        return f"user: {self.username} following: {self.following} liked: {self.liked_post} followers: {self.followers}"

class Post(models.Model):
    post_creator=models.ForeignKey(User,on_delete=models.CASCADE)
    post_content=models.CharField(max_length=500)

    #likes=models.IntegerField(default=0)
    timestamp=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"Post by: {self.post_creator}"
