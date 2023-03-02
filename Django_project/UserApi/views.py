from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def Add(num1, num2):
    sum = int(num1) + int(num2)
    return sum 

def Subtract(num1 , num2):
    sub = int(num1)- int(num2)
    return sub

def Multiply(num1,num2):
    mult = int(num1) * int(num2)
    return mult

def division(num1,num2):
    div = int(num1) / int(num2)
    return div

def index(request):
    form  = """
    <form method="GET">
    <input type='text' name='num1'>
    <input type='text' name='num2'>
    <button name='add'>+</button>
    <button name='sub'>-</button>
    <button name='mul'>*</button>
    <button name='div'>/</button>
    </form>
    """
    result = ""
    if request.method == 'GET':
        num1 = request.GET.get('num1')
        num2 = request.GET.get('num2')
        print(request.GET)
        # if 'Submit' in request.POST:
        if 'add' in request.GET:
            result = Add(num1 , num2)
        elif 'sub'in request.GET:
            result = Subtract(num1, num2)
        elif 'mul' in request.GET:
            result= Multiply(num1, num2)
        elif 'div' in request.GET:
            result= division(num1, num2)
        else:
            result = ""
    return HttpResponse(f"<html>{form} <h2>Result: {result}</h2><html>")











