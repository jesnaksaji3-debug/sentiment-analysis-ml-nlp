from django.db import models

class User(models.Model):
    uid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    gender = models.CharField(max_length=20)
    contact = models.CharField(max_length=20)
    place = models.CharField(max_length=20)
    district = models.CharField(max_length=50)

    class Meta:
        db_table = "user"

class Login(models.Model):
    lid = models.AutoField(primary_key=True)
    uid = models.CharField(max_length=50)
    uname = models.CharField(max_length=50)
    upass = models.CharField(max_length=50)
    utype = models.CharField(max_length=30)
    
    class Meta:
        db_table = "login"

class Review(models.Model):
    rid = models.AutoField(primary_key=True)
    pdtname = models.CharField(max_length=100)
    review = models.TextField()
    rating = models.IntegerField()
    uid = models.CharField(max_length=50)

    class Meta:
        db_table = "review"
