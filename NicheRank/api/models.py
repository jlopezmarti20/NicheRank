from django.db import models

# Create your models here.

# user info
class userInfo(models.Model):
    name= models.CharField(max_length=100)

# Model for their top songs
class Songs(models.Model):
    country=models.TextField()
    uri=models.TextField()
    name=models.TextField()
    artist=models.TextField()
    explicit=models.TextField()
    genres=models.TextField()
    danceability=models.FloatField()
    energy=models.FloatField()
    key=models.IntegerField()
    loudness=models.FloatField()
    speechiness=models.FloatField()
    acoustics=models.FloatField()
    instrumentalness=models.FloatField()
    liveliness=models.FloatField()
    valence=models.FloatField()
    tempo=models.FloatField()
    duration_seconds=models.FloatField()
