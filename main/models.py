from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
import datetime

# Create your models here.

class SavedOffers(models.Model):
    title = models.CharField(max_length=350)
    href = models.CharField(max_length=350)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    job_salary = models.CharField(max_length=200)
    contract_type = models.CharField(max_length=150)
    site = models.CharField(max_length=100)
    keyword = models.CharField(max_length=150, default="")
    user = models.CharField(max_length=100, default="")
    foreign = models.IntegerField(default=0)

    def __str__(self):
        return self.user

class TestingOffers(models.Model):
    title = models.CharField(max_length=350)
    href = models.CharField(max_length=350)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    job_salary = models.CharField(max_length=200)
    contract_type = models.CharField(max_length=150)
    site = models.CharField(max_length=100)
    keyword = models.CharField(max_length=150, default="")
    published_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.title#, self.href, self.company_name, self.location, self.site, self.keyword

class Offers(models.Model):
    title = models.CharField(max_length=100)
    company_name = models.CharField(max_length=200)
    location = models.CharField(max_length=100)
    job_position = models.CharField(max_length=150)
    job_salary = models.CharField(max_length=200)
    contract_type = models.CharField(max_length=150)
    job_description = models.TextField(default="")
    published_date = models.DateField(default=datetime.date.today)
    genre = models.CharField(max_length=100, default="")

    def __str__(self):
        return self.title

class Test(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
 
class ToDoList(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Item(models.Model):
    todolist = models.ForeignKey(ToDoList, on_delete=models.CASCADE)
    text = models.CharField(max_length=300)
    complete = models.BooleanField()

    def __str__(self):
        return self.text

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']