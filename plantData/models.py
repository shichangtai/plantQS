from __future__ import unicode_literals

from django.db import models

# Create your models here.
class User(models.Model):
    userId=models.AutoField(primary_key=True)
    user_name=models.CharField(max_length=255)
    user_passWd=models.CharField(max_length=20)
    gender=models.CharField(max_length=2, choices=[('M','Male'),('F','Female')])
    name=models.CharField(max_length=30,blank=True,null=True)
    birth=models.CharField(max_length=30,blank=True,null=True)
    
class Question(models.Model):
    questionId=models.AutoField(primary_key=True)
    user_id=models.ForeignKey(User)
    que_time=models.CharField(max_length=50,blank=True,null=True)
    imge_other1=models.CharField(max_length=150,blank=True,null=True)
    describe=models.TextField(max_length=500,blank=True,null=True)    

    
    
class Plant(models.Model):
    plantId=models.AutoField(primary_key=True)
    plant_name=models.CharField(max_length=30)
    plant_image1=models.CharField(max_length=150,blank=True,null=True)
    plant_image2=models.CharField(max_length=150,blank=True,null=True)
    plant_image3=models.CharField(max_length=150,blank=True,null=True)
    other_details=models.CharField(max_length=500,blank=True,null=True)     
    
class Expert(models.Model):
    expertId=models.AutoField(primary_key=True)
    exp_acount=models.CharField(max_length=20)
    exp_password=models.CharField(max_length=20)
    exp_mail=models.EmailField(blank=True)
    exp_name=models.CharField(max_length=10,blank=True)
    exp_gender=models.CharField(max_length=2, choices=[('M','Male'),('F','Female')])     
    
class Answer(models.Model):
    ansId=models.AutoField(primary_key=True)
    que_id=models.ForeignKey(Question)
    pla_id=models.ForeignKey(Plant)
    exp_id=models.ForeignKey(Expert)
    ans_credit=models.CharField(max_length=2,choices=[('l','low'),('m','middle'),('h','high')],blank=True)
    ans_time=models.DateField(blank=True)
    user_reply=models.TextField(max_length=200,blank=True)