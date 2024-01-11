from django.contrib import admin
from .models import *
# Register your models here.
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display=['id','course_name']

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display=['id','course','question','answer','option_one','option_two','option_three','option_four']

@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display=['id','name','email','mobile']