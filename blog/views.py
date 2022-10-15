from http.client import HTTPResponse
from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import SignUpForm,LogInForm,BlogForm
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .models import Blog
from django.contrib.auth.models import Group

# Create your views here.
def home(request):
    posts=Blog.objects.all()
    return render(request, 'blog/home.html',{'posts':posts})

def about(request):
    return render(request, 'blog/about.html')

def contact(request):
    return render(request, 'blog/contact.html')

def dashboard(request):
    if request.user.is_authenticated:
        posts=Blog.objects.all()
        full_name=request.user.get_full_name()
        grps=request.user.groups.all()
        return render(request, 'blog/dashboard.html',{'posts':posts,'fullname':full_name,'grps':grps})
    else:
        return HttpResponseRedirect('/login/')

def signup(request):
    if not request.user.is_authenticated:
        if request.method =="POST":
            form=SignUpForm(request.POST)
            if form.is_valid():
                user=form.save()
                group=Group.objects.get(name='Author')
                user.groups.add(group)
                messages.success(request,"Congratulation!! signup successfully..")
        else:
            form=SignUpForm()
        return render(request, 'blog/signup.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')

def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            form=LogInForm(request=request,data=request.POST)
            if form.is_valid():
                uname=form.cleaned_data['username']
                upass=form.cleaned_data['password']
                user=authenticate(username=uname,password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,"congrats!! Successfully login")
                    return HttpResponseRedirect('/dashboard/')
        else:
            form=LogInForm()
        return render(request, 'blog/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/dashboard/')
    


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/')

def add_post(request):
    if request.method=="POST":
        form=BlogForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Post added successfully !')
    else:
        form=BlogForm()
    return render(request,'blog/addpost.html',{'form':form})

def edit_post(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            x=Blog.objects.get(pk=id)
            form=BlogForm(request.POST,instance=x)
            if form.is_valid():
                form.save()
                messages.success(request,"Post updated successfully !")
                return HttpResponseRedirect('/dashboard/')
        else:
            x=Blog.objects.get(pk=id)
            form=BlogForm(instance=x)
        return render(request,'blog/updatepost.html',{'form':form})
    else:
        return HttpResponseRedirect('/login/')


def delete_post(request,id):
    if request.user.is_authenticated:
        if request.method=="POST":
            x=Blog.objects.get(pk=id)
            x.delete()
            messages.info(request,"Post deleted successfully !")
            return HttpResponseRedirect('/dashboard/')
    else:
       return HttpResponseRedirect('/login/')
            
