from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
import requests as request
from random import randint


def index(req):
    url = "https://raw.githubusercontent.com/dwyl/quotes/main/quotes.json"

    response = request.get(url)
    quote = author = ''

    if response.status_code == 200:
        quotes = response.json()
        if quotes:
            ri = randint(0, len(quotes) - 1)
            quote = quotes[ri]['text']
            author = quotes[ri]['author']
            res = dict({'quote':quote, 'author':author})
    return render(req, 'index.html', res)


def loginUser(req):
    if req.method == "POST":
        if req.POST.get('usrId') == '' or req.POST.get('usrPsd') == '':
            messages.info(req, 'Enter All Fields')
            return redirect('login')
        else:
            id = req.POST.get('usrId')
            psd = req.POST.get('usrPsd')
            user = auth.authenticate(username=id, password=psd)
            if user is not None:
                auth.login(req, user)
                return redirect('home')
            else:
                messages.info(req, 'InValid Credentials')
                return redirect('login')
    else:
        return render(req, 'login.html')
    

def logoutUser(req):
    auth.logout(req)
    return redirect('/')


def register(req):
    if req.method == "POST":
        if req.POST.get('usrFname') == '' or req.POST.get('usrLname') == '' or req.POST.get('usrEmail') == '' or req.POST.get('usrId') == '' or req.POST.get('usrPsd') == '' or req.POST.get('usrRePsd') == '':
            messages.info(req, "All Fields Must be Entered")
            return redirect('register')
        else:
            fname = req.POST.get('usrFname')
            lname = req.POST.get('usrLname')
            email = req.POST.get('usrEmail')
            id = req.POST.get('usrId')
            psd = req.POST.get('usrPsd')
            repsd = req.POST.get('usrRePsd')

            if psd == repsd:
                if User.objects.filter(email=email).exists():
                    messages.info(req, "Email Already Registered")
                    return redirect('register')
                elif User.objects.filter(username=id).exists():
                    messages.info(req, "UserID Already Used")
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=id,first_name=fname, last_name=lname, email=email, password=psd)
                    user.save()
                    return redirect('login')
            else:
                messages.info(req, "Password Must Match")
                return redirect('register')
    else:
        return render(req, 'register.html')


def home(req):
    return render(req, 'home.html')