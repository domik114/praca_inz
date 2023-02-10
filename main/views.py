from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Offers, Test, CreateUserForm, TestingOffers, SavedOffers
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, auth
from django.db.models import Q
from django.contrib.auth.decorators import login_required

from bs4 import BeautifulSoup as bs
from selenium.webdriver import Chrome, ChromeOptions
import time
from selenium.webdriver.common.keys import Keys

from .skrypty import pracuj, OLX

# Create your views here.

def home(request): 
    context = {}
    return render(request, "main/home.html", context)

def base(request, id):
    ls = Offers.objects.get(id=id)
    return render(request, "main/list.html", {"ls": ls})

@login_required(login_url="/login")
def saved(request, id):
    if id == 1:
        data = SavedOffers.objects.filter(user=request.user.username).values()
        
        context = {"data": data}
        return render(request, "main/saved.html", context)
        
    data = SavedOffers.objects.filter(foreign=id, user=request.user.username).values()
    
    for d in data:
        if d['foreign'] == id and d['user'] == request.user.username:
            SavedOffers.objects.filter(foreign=id, user=request.user.username).delete()

            display = SavedOffers.objects.filter(user=request.user.username).values()
            context = {"data": display}
            return render(request, "main/saved.html", context)

    to_save = TestingOffers.objects.filter(id=id).values()

    for ts in to_save:
        save = SavedOffers(title=ts["title"], contract_type=ts["contract_type"], href=ts["href"], company_name=ts["company_name"], job_salary=ts["job_salary"], location=ts["location"], site=ts["site"], keyword=ts["keyword"], user=request.user.username, foreign=id)
        save.save()
    
    data = SavedOffers.objects.filter(user=request.user.username).values()       
            
    context = {"data": data}
    return render(request, "main/saved.html", context)

def search_bar(request):
    if request.method == "POST":
        searched = request.POST["job"]
        localization = request.POST["localization"]

        praca = pracuj(searched, localization)

        praca_return = []
        db = TestingOffers.objects.all().order_by('-id').values()

        i = 0 
        for index in range(len(db)):
            if i == len(praca):
                break

            p = {
                "id": db[index]["id"],
                "title": db[index]["title"],
                "contract": db[index]["contract_type"],
                "location": db[index]["location"],
                "company_name": db[index]["company_name"],
                "href": db[index]["href"]
            }

            praca_return.append(p)

            i += 1

        olx = OLX(searched, localization)

        olx_return = []
        db = TestingOffers.objects.all().order_by('-id').values()

        i = 0 

        for index in range(len(db)):
            if i == len(olx):
                break

            if db[index]["title"] == "" or db[index]["title"] is None:
                continue

            o = {
                "id": db[index]["id"],
                "title": db[index]["title"],
                "contract": db[index]["contract_type"],
                "location": db[index]["location"],
                "job_salary": db[index]["job_salary"],
                "href": db[index]["href"]
            }

            olx_return.append(o)

            i += 1

        context = {"searched": searched, 'olx': olx_return, "pracuj": praca_return}
        return render(request, "main/search_bar.html", context)
    else:
        context = {}
        return render(request, "main/search_bar.html", context)



#def register(request):
#    form = CreateUserForm()
#
#    if request.method == 'POST':
#        #form = CreateUserForm(request.POST)
#        first_name = request.POST['first_name']
#        last_name = request.POST['last_name']
#        username = request.POST['username']
#        password1 = request.POST['password1']
#        password2 = request.POST['password2']
#        email = request.POST['email']
#
#        if password1 == password2:
#            if User.objects.filter(username=username).exists():
#                print("Username taken")
#            elif User.objects.filter(email=email).exists():
#                print("Email taken")
#            else:
#                user = User.objects.create_user(username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
#                user.save()
#                print("User created!")
#        else:
#            print("Password nor matching")
#
#        return redirect('/')
#    else:
#        context = {"form": form}
#        return render(request, "main/register.html", context)

#def login(request):
#    context = {}
#    return render(request, "main/login.html", context)