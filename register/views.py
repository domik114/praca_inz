from django.shortcuts import render, redirect
from register.forms import RegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

# Create your views here.
@login_required(login_url="/login")
def account_list(request):
    users = User.objects.all().order_by('id')

    context = {"users": users}
    return render(request, "register/accounts_list.html", context)

def account_change(request, id):


    context = {}
    return render(request, "register/user_change.html", context)

@login_required(login_url="/login")
def account(request, id):
    username = request.user.username
    first_name = request.user.first_name
    last_name = request.user.last_name

    context = {"username": username, "first_name": first_name, "last_name": last_name}
    return render(request, "register/account.html", context)

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)

        if form.is_valid():
            form.save()
        else:
            form = RegisterForm()

            context = {"form": form}
            return render(request, "register/register.html", context)

        return redirect("/")
    else:
        form = RegisterForm()
    
    context = {"form": form}
    return render(request, "register/register.html", context)
