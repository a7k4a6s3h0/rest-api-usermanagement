from django.shortcuts import render,redirect
import requests
from django.contrib import messages
import base64
import os
# Create your views here.

def user_signup(request):
    if request.method == 'POST':

        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = firstname +' '+ lastname 
        email = request.POST.get('email')
        phone_no = request.POST.get('number')
        profile_pic = request.FILES['picture']
        password = request.POST.get('password')
        print(username,profile_pic)
        # image_path = os.path.abspath(profile_pic.name)
        # print(image_path,"path")
        with open(r"C:\Users\User\Pictures\Screenshots\mongogbass5.png", 'rb') as f:
            image_data = f.read()
            image_data_base64 = base64.b64encode(image_data).decode('utf-8')
        payload = {
            'username':username,
            'email':email,
            'password':password,
            'profile_photo':image_data_base64,
            "mobile_no":phone_no
        }
        
        response = requests.post('http://localhost:8000/api/register/',payload).json()
    
        for k, v in response.items():
            response2 = v
        if response2 == None:
            messages.error(request,'user is already exists')
            return redirect('user_signup')
        else:
           return redirect('user_login')   

    return render(request,'user_signup.html')


def user_home(request):
    info = request.COOKIES.get('jwt')
    if info:
        print(info,"info")
        payload = {
            'token_id':info
        }
        response = requests.get('http://localhost:8000/api/home/',payload).json()
        for k, i in response.items():
            if i == None:
                return redirect('user_login')
        dic = {
            'username':response['username'],
            'email':response['email'],
            'phone':response['mobile_no'],

        }         
        return render(request,'user_home.html',{'dict':dic}) 
    return redirect('user_login')    


def user_login(request):
    if request.COOKIES.get('jwt'):
        return redirect('user_home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        payload = {
            'username':username,
            'password':password
        }
        response = requests.post('http://localhost:8000/api/login/',payload).json()
        print(response,"in login testapi")
        for k, v in response.items():
            response2 = v
        if response2 == None:
            print("in login none")
            messages.error(request,"invalid username or password")
            return redirect("user_login")
        else:
            page = redirect('user_home') 
            page.set_cookie('jwt',response2)
            return page    

    return render(request,'user_login.html')       


# def user_logout(request):
#     response = requests.post('http://localhost:8000/api/logout/').json()
#     print(response)  
#     return redirect('user_login')

def user_logout(request):
   res = redirect('user_login')   
   res.delete_cookie('jwt')
   return res