from django.shortcuts import render,redirect
from .forms import *
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import requests
import random

# Create your views here.
def index(request):
    if request.method=='POST': #root condition
        if request.POST.get('signup')=='signup':
            newuser=signupform(request.POST)
            if newuser.is_valid():
                newuser.save()
                print("Signup Successfully!")
                messages.success(request,"Signup Successfully!")
            else:
                print(newuser.errors)
                messages.error(request,newuser.errors)
        elif request.POST.get('signin')=='signin':
            unm=request.POST['username']
            pas=request.POST['password']

            user=usersignup.objects.filter(username=unm,password=pas)
            
            if user:
                print("Login successfully!")
                messages.success(request,"Login Success!")
                uid=usersignup.objects.get(username=unm)
                print("UserID:",uid.id)
                request.session['user']=unm
                request.session['userid']=uid.id
                return redirect('notes')
            else:
                messages.error(request,"Oops... Login faild....Try again!")
    return render(request,'index.html')


#@login_required(login_url='/')
def notes(request):
    user=request.session.get('user')
    if request.method=='POST':
        newnotes=notesform(request.POST, request.FILES)
        if newnotes.is_valid():
            newnotes.save()
            print("Your notes has been submitted")
        else:
            print(newnotes.errors)
    return render(request,'notes.html',{'user':user})


def profile(request):
    user=request.session.get('user')
    userid=request.session.get('userid')
    cuser=usersignup.objects.get(id=userid)
    if request.method=='POST':
        updateprofile=updateForm(request.POST)
        if updateprofile.is_valid():
            updateprofile=updateForm(request.POST,instance=cuser)
            updateprofile.save()
            print("Your profile has been updated!")
            return redirect('notes')
        else:
            print(updateprofile.errors)
    return render(request,'profile.html',{'user':user,'cuser':cuser})

def about(request):
    return render(request,'about.html')

def contact(request):
    if request.method=='POST':
        newcontact=contactForm(request.POST)
        if newcontact.is_valid():
            newcontact.save()

            # Email send
            send_mail(subject="Thank you for contacting us.",message=f"Dear User\n\nThank you for connecting us!\nWe will contact you soon!\n\nThanks & Regards\n+916352613163 | princesoni2701@gmail.com", from_email="princesoni2701@gmail.com", recipient_list=[request.POST['email']])
            print("Data saved.")

             #SMS Send
            otp=random.randint(1111,9999)
            url = "https://www.fast2sms.com/dev/bulkV2"
            querystring = {"authorization":"KEodGZf5czOn3eCxJPkWAFHQUYtS86Rbmrv1MyuViag4hs7N2DujvzKSw5MN9mRryb3LC4DsIHiWph78","variables_values":f"{otp}","route":"otp","numbers":f"{request.POST['phone']}"}
            headers = {
                'cache-control': "no-cache"
            }
            response = requests.request("GET", url, headers=headers, params=querystring)
            print(response.text)
        else:
            print(newcontact.errors)
    return render(request,'contact.html')

def userlogout(request):
    logout(request)
    return redirect("/")