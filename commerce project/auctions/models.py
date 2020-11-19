from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Categories(models.Model):
    category_name=models.CharField(max_length=30)

    def __str__(self):
        return f"{self.pk}  {self.category_name}"


class Listing(models.Model):
    user=models.CharField(max_length=64)
    title=models.CharField(max_length=64,unique=True)
    desc=models.TextField()
    category=models.ForeignKey(Categories,on_delete=models.CASCADE)
    img_link = models.URLField(default=None, blank=True, null=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} {self.user} {self.title}"

class Bid(models.Model):
    bid_item=models.OneToOneField(Listing,to_field="title",primary_key=True,on_delete=models.CASCADE)
    user=models.CharField(max_length=64)
    bid_value=models.IntegerField()

    def __str__(self):
        return f"{self.bid_item} {self.user} {self.bid_value}"

class Comment(models.Model):
    comm_id=models.ForeignKey(Listing,on_delete=models.CASCADE,null=True)
    user=models.CharField(max_length=64)
    comment=models.CharField(max_length=120)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.comm_id} {self.user} {self.comment}"

class Watchlist(models.Model):
    user=models.CharField(max_length=64)
    item=models.ManyToManyField(Listing)

    def __str__(self):
        return f"{self.item} {self.user}"

class Winner(models.Model):
    title=models.CharField(max_length=64)
    seller=models.CharField(max_length=64)
    user=models.CharField(max_length=64)
    final_bid=models.IntegerField()

    def __str__(self):
        return f"{self.title} {self.user} {self.final_bid}"
