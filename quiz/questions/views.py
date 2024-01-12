from django.shortcuts import render,redirect,HttpResponseRedirect
from .models import *
from .forms import RegistrationForm
from django.contrib import messages
import os
from twilio.rest import Client
# Create your views here.

def registration(request):
    if request.method=='POST':
        users=Registration.objects.all()
        registration_form=RegistrationForm(request.POST)
        if registration_form.is_valid():
            
            global user_name
            global user_email
            global user_mobile

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
        
            request.session[str(user_name)]=user_name
            request.session[str(user_email)]=user_email
            request.session[str(user_mobile)]=user_mobile
            request.session.set_expiry(0)
            return redirect('registration_otp')

    else:
        registration_form=RegistrationForm()
        return render(request,'questions/registration.html',{'registration_form':registration_form}) 

def registration_otp(request):
    global user_name
    global user_email
    global user_mobile
    if str(user_mobile) in request.session:
        account_sid = "ACbf04a8f8f4e4f25e7eda3310e7a7b17f"
        auth_token = "291298433eb51fa82e68433a2185846e"
        verify_sid = "VA9920ccda8a38f9924baffdae6e89d434"
        mobile=request.session[str(user_mobile)]
        verified_number = "+91"+str(mobile)
        client = Client(account_sid, auth_token)
        if request.method=='POST':
            otp_code = request.POST.get('otp')

            verification_check = client.verify.v2.services(verify_sid) \
                .verification_checks \
                .create(to=verified_number, code=otp_code)
            if verification_check.status == 'approved':
                user_name=request.session[str(user_name)]
                user_email=request.session[str(user_email)]
                user_mobile=request.session[str(user_mobile)]
                user=Registration(name=user_name,email=user_email,mobile=user_mobile)
                user.save()
                messages.success(request,'Verified Successfully')
                return HttpResponseRedirect('/home')

        else:

            verification = client.verify.v2.services(verify_sid) \
                .verifications \
                .create(to=verified_number, channel="sms")
            print(verification.status)
            return render(request,'questions/registration_otp.html')
    else:
        messages.warning(request,'Login First')
        return HttpResponseRedirect('/login')


def login(request):
    if request.method=='POST':
        users=Registration.objects.all()
        global user_mobile
        user_mobile=request.POST.get('mobile')
        for user in users:
            if user_mobile == str(user.mobile):
                request.session[str(user_mobile)]=user_mobile
                request.session.set_expiry(0)
                return HttpResponseRedirect('/login_otp')
            else:
                pass
        messages.warning(request,"You don't have an account. Register Here!")
        return HttpResponseRedirect('/')

    else:
        return render(request,'questions/login.html') 
    
def login_otp(request):
    global user_mobile
    if str(user_mobile) in request.session:
        account_sid = "ACbf04a8f8f4e4f25e7eda3310e7a7b17f"
        auth_token = "291298433eb51fa82e68433a2185846e"
        verify_sid = "VA9920ccda8a38f9924baffdae6e89d434"
        mobile=request.session[str(user_mobile)]
        verified_number = "+91"+str(mobile)
        client = Client(account_sid, auth_token)
        if request.method=='POST':
            otp_code = request.POST.get('otp')

            verification_check = client.verify.v2.services(verify_sid) \
                .verification_checks \
                .create(to=verified_number, code=otp_code)
            if verification_check.status == 'approved':
                messages.success(request,'Logged in Successfully')
                return HttpResponseRedirect('/home')

        else:

            verification = client.verify.v2.services(verify_sid) \
                .verifications \
                .create(to=verified_number, channel="sms")
            print(verification.status)
            return render(request,'questions/login_otp.html')
    else:
        messages.warning(request,'Login First')
        return HttpResponseRedirect('/login')


def home(request):
    global user_mobile
    if str(user_mobile) in request.session:
        courses=Course.objects.all()
        return render(request, 'questions/home.html',{'courses':courses})
    else:
        messages.warning(request,'Login First')
        return HttpResponseRedirect('/login')


def quiz(request,id):
    global user_mobile
    if str(user_mobile) in request.session:
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
    else:
        messages.warning(request,'Login First')
        return HttpResponseRedirect('/login')

def result(request,id):
    global user_mobile
    if str(user_mobile) in request.session:
        marks=request.session.get(str(id))
        return render(request,'questions/result.html',{'marks':marks})
    else:
        messages.warning(request,'Take a quiz first')
        return HttpResponseRedirect('/home')