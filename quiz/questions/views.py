from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import *
from .forms import RegistrationForm
from django.contrib import messages
import os
from twilio.rest import Client
# Create your views here.
def otp(request):
    account_sid = "ACbf04a8f8f4e4f25e7eda3310e7a7b17f"
    auth_token = "b741c56f844b22c94ef7d39232b5be7a"
    verify_sid = "VA9920ccda8a38f9924baffdae6e89d434"
    mobile=request.session['user_mobile']
    verified_number = "+91"+str(mobile)
    client = Client(account_sid, auth_token)
    if request.method=='POST':
        otp_code = request.POST.get('otp')

        verification_check = client.verify.v2.services(verify_sid) \
            .verification_checks \
            .create(to=verified_number, code=otp_code)
        if verification_check.status == 'approved':
            user_name=request.session['user_name']
            user_email=request.session['user_email']
            user_mobile=request.session['user_mobile']
            user=Registration(name=user_name,email=user_email,mobile=user_mobile)
            user.save()
            messages.success(request,'Verified Successfully')
            return HttpResponseRedirect('/home')
    
    else:
        
        verification = client.verify.v2.services(verify_sid) \
            .verifications \
            .create(to=verified_number, channel="sms")
        print(verification.status)
        return render(request,'questions/otp.html')



def registration(request):
    if request.method=='POST':
        users=Registration.objects.all()
        registration_form=RegistrationForm(request.POST)
        if registration_form.is_valid():
            user_name=registration_form.cleaned_data['name']
            user_email=registration_form.cleaned_data['email']
            user_mobile=registration_form.cleaned_data['mobile']

            if len(str(user_mobile))!=10:
                messages.error(request,'Enter a valid mobile number')
                return HttpResponseRedirect('/')
            for user in users:
                if user_mobile==user.mobile:
                    messages.warning(request,'This mobile is already registered.')
                    return HttpResponseRedirect('/')
        
            request.session['user_name']=user_name
            request.session['user_email']=user_email
            request.session['user_mobile']=user_mobile
            return redirect('otp')

    else:
        registration_form=RegistrationForm()
        return render(request,'questions/registration.html',{'registration_form':registration_form}) 

def login(request):
    if request.method=='POST':
        pass

    else:
        # login_form=RegistrationForm()
        return render(request,'questions/login.html') 

def home(request):
    courses=Course.objects.all()
    return render(request, 'questions/home.html',{'courses':courses})

def quiz(request,id):
    count=0
    if request.method=='POST':
        questions=Question.objects.filter(course=id).values()
        for item in questions: 
            answer=request.POST.get(str(item['id']))
            if str(answer)==str(item['answer']):
                count+=1
        request.session[str(id)]=count
        return redirect('result',id)
    else:
        questions=Question.objects.filter(course=id).values()
    return render(request, 'questions/quiz.html',{'questions':questions})

def result(request,id):
    marks=request.session.get(str(id))
    return render(request,'questions/result.html',{'marks':marks})