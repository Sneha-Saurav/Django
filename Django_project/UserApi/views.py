from django.shortcuts import redirect, render
from django.http import HttpResponse
from UserApi.models import Blog
from django import forms
from .forms import BlogForm, UserForm, ChangePasswordForm
from django.contrib.auth import authenticate
from datetime import datetime
from django.contrib import messages
from django.contrib.auth import authenticate, login as authlogin, logout
from cartapp.forms import *
from django.contrib.auth.decorators import permission_required
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
from django.views import View

format=  "%Y-%m-%d"

class BlogFormView(View):
    form  = BlogForm()
    def get(self, request):
        form  = BlogForm(request.POST)
        return render(request, 'create.html',{'form':form})

    def post(self, request):
        form  = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            blogs = Blog.objects.all()
        return render(request, 'list.html', {'blogs':blogs})
    
class BlogView(View):
    def get(self,request):
        blogs  = Blog.objects.all()
        return render(request, 'list.html', {'blogs':blogs})
    
    # def delete(self,request, **kwargs):
    #     print(request.method)
    #     try:
    #         if pk:= kwargs.get('id'):
    #             edit_blog  = Blog.objects.get(pk=pk)
    #             edit_blog.delete()
    #             return redirect('/blog/list')  # use reverse here 
    #     except:
    #         error_msg= "Blog not found"
    #     blogs  = Blog.objects.all()      
    #     return render(request, 'blog_details.html',{'blogs':blogs, 'msg':error_msg})

        


       
       
    


def home_blog(request):
    return render(request,'blog_index.html')


def register_user(request):
    form = RegisterForm()
    if request.method == 'POST':
        # print(request.POST)
        # import pdb; pdb.set_trace()
        print(request.user)
        username = request.POST.get('username')
        password = request.POST.get('password')
        email  =  request.POST.get('email')
        user = User.objects.create_user(username, password =password, email=email)
        user.save()
        messages.success(request,'Register Successfully')

    return render(request, 'register_user.html',{'form':form})

def blog_login(request):
    form = LoginForm()
    username = request.POST.get('username')
    password = request.POST.get("password")
    user = authenticate(request,username=username, password=password)
    print(user)
    if user is not None:
        authlogin(request,user)
        messages.success(request,'Login Successfully')
        
    else:
        print("error")
        messages.error(request, 'Invalid Credentials')
    return render(request, 'blog_login.html', {'form': form})


@login_required(login_url='/user/blog/login')
def user_profile(request):
    return render(request,'profile.html')


def update_user(request,**kwargs):
    form  = ChangePasswordForm()
    if request.method == 'POST':
        if pk:= kwargs.get('id'):
            password =request.POST.get('password')
            confirm_pass = request.POST.get('confirm_password')
            print(password)
            if password == confirm_pass:
                print(pk)
                print("yes done")
                user = User.objects.get(id=pk)
                print(user)
                user.set_password(password)
            
                user.save()
                messages.success(request,'Set Successfully')
        else:
            messages.error(request,'Password did not match')
    return render(request, 'change_pass.html', {'form':form})


def logout_user_blog(request):
    logout(request)
    print(request.user)
    return redirect('/home') 



@permission_required('UserApi.add_blog',raise_exception=True)
def blog_create(request):
    blogform  = BlogForm()
    if request.method  == 'POST':
        blogform  = BlogForm(request.POST)
        # request_date  =  request.POST['create_date']
        # datetime.strptime(request_date, format)
        if blogform.is_valid():
            # blog = blogform.save()
            blogform.save()
            return redirect('/blog/list')
        print(request.POST)
    return render(request, 'create.html',{'form':blogform})


def get_blogs(request):
    if request.method  == 'GET':
            blogs  = Blog.objects.all()
    return render(request, 'list.html', {'blogs':blogs})


@permission_required('UserApi.can_publish', raise_exception=True)
def publish_blog(request, **kwargs):
    if request.method == 'GET':
        if id:= kwargs.get('id'):
                blog = Blog.objects.get(id=id)
                blog.is_published = True
                blog.save()
                messages.success(request,'Blog Published!!')
    return redirect('/blog/list')


def get_published_blog(request):
    blogs = Blog.objects.filter(is_published=True)
    return render(request, 'list.html', {'blogs':blogs})



def get_blog(request, **kwargs):
    print(request.method)
    if request.method == 'GET':
        print("hello")
        print(request.GET)
        if id:= kwargs.get('id'):
            blog = Blog.objects.get(id=id)
    return render(request,'blog_details.html',{'blog':blog})


@permission_required('UserApi.change_blog',raise_exception=True)
def blog_edit(request, **kwargs):
    blogform  = BlogForm()
    if request.method  == 'POST':
        if pk:= kwargs.get('pk'):
            edit_blog  = Blog.objects.get(pk=pk)
            print(edit_blog)
            blogform  = BlogForm(request.POST, instance=edit_blog)  # instance is like object we want to edit for a specifiv object in modals
            if blogform.is_valid():
                blogform.save()
                return redirect('/blog/list')
            print(request.POST)
    return render(request, 'edit.html',{'form':blogform})

@permission_required('UserApi.delete_blog',raise_exception=True)
def blog_delete(request, **kwargs):
    error_msg = ""
    if request.method  == 'GET':
        try:
            if pk:= kwargs.get('pk'):
                edit_blog  = Blog.objects.get(pk=pk)
                edit_blog.delete()
                return redirect('/blog/list')  # use reverse here 
        except:
            error_msg= "Blog not found"

    blogs  = Blog.objects.all()      
    return render(request, 'list.html',{'blogs':blogs, 'msg':error_msg})


def user_create(request):
    userform = UserForm()
    if request.method  == 'POST':
        userform = UserForm(request.POST)
        if userform.is_valid():
            userform.save()
    return render(request, 'user_create.html', {'form':userform})


























# def Add(num1, num2):
#     sum = int(num1) + int(num2)
#     return sum 

# def Subtract(num1 , num2):
#     sub = int(num1)- int(num2)
#     return sub

# def Multiply(num1,num2):
#     mult = int(num1) * int(num2)
#     return mult

# def division(num1,num2):
#     div = int(num1) / int(num2)
#     return div

# def index(request):
#     num1 = request.GET.get('num1', '')
#     num2 = request.GET.get('num2', '')
#     form  = f"""
#     <form method="GET">
#     <input type='text' name='num1' value={num1}>
#     <input type='text' name='num2' value={num2}>
#     <button name='add'>+</button>
#     <button name='sub'>-</button>
#     <button name='mul'>*</button>
#     <button name='div'>/</button>
#     </form>
#     """
#     result = ""
#     if request.method == 'GET':
#         print(request.GET)
#         # if 'Submit' in request.POST:
#         if 'add' in request.GET:
#             result = Add(num1 , num2)
#         elif 'sub'in request.GET:
#             result = Subtract(num1, num2)
#         elif 'mul' in request.GET:
#             result= Multiply(num1, num2)
#         elif 'div' in request.GET:
#             result= division(num1, num2)
#         else:
#             result = ""
#     return HttpResponse(f"<html>{form} <h2>Result: {result}</h2><html>")





# def get_blog(request, blog_id):
#     try:
#         result  = Blog.objects.get(pk=blog_id)
#     except Blog.DoesNotExist:
#         raise Http404("Blog does not exist.")
#     print(result.title)
#     return HttpResponse(f"<h1>{result.title}</h1><p>{result.description}</p>")


# def solve(request):
#     form = CalculatorForm()
#     num1 = request.GET.get('num1', '')
#     num2 = request.GET.get('num2', '')
#     result = ""
#     if request.method == 'GET':
#         print(request.GET)
#         if 'add' in request.GET:
#             result = Add(num1 , num2)
#         elif 'sub'in request.GET:
#             result = Subtract(num1, num2)
#         elif 'mul' in request.GET:
#             result= Multiply(num1, num2)
#         elif 'div' in request.GET:
#             result= division(num1, num2)
#         else:
#             result = ""

#     return render(request,'index.html',{'form':form,'result':result})


# class CalculatorForm(forms.Form):
#     num1  = forms.CharField(label="Enter the first number", max_length=50 )
#     num2 = forms.CharField(label="Enter the second number", max_length=50)

