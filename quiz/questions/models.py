from django.db import models
# Create your models here.
class Course(models.Model):
    course_name=models.CharField(max_length=100)

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    question=models.CharField(max_length=100)
    answer=models.IntegerField()
    option_one=models.CharField(max_length=100)
    option_two=models.CharField(max_length=100)
    option_three=models.CharField(max_length=100, blank=True)
    option_four=models.CharField(max_length=100, blank=True)
    
class Registration(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    mobile=models.IntegerField()
    