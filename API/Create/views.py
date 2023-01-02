from django.shortcuts import render,redirect
#from django.contrib.auth.models import User
from .models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.http import JsonResponse
from django.http import HttpResponse
import jwt , datetime
# Create your views here.

from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_authtoken.models import AuthToken
from .serializers import UserSerializer, RegisterSerializer
from rest_framework.views import APIView
from rest_framework.decorators import parser_classes
from rest_framework.parsers import JSONParser , MultiPartParser, FormParser
from django.core.files.base import ContentFile
from django.http import QueryDict
from io import BytesIO
from PIL import Image
import imghdr
import base64
import random

# Register 

class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args, **kwargs):
        image_data = base64.b64decode(request.data['profile_photo'])
        im = Image.open(BytesIO(image_data))
        im = im.convert('RGB')
        image_type = imghdr.what(None, image_data)
        # Generate a filename for the image
        number = str(random.randint(10, 99))
        filename = 'image'+number+'.' + image_type
        # Print the decoded filename
        print(filename)
        #updating my data
        edited_data = {
            'username':request.data['username'],
            'email':request.data['email'],
            'password':request.data['password'],
            'profile_photo':filename,
            'mobile_no':request.data['mobile_no']
        }
        data = QueryDict('', mutable=True)
        data.update(edited_data)
        print(data,"edited data")
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)   
        serializer.save()
        user = serializer.data
        return Response({"username":user['username']})
        # else:
        #     print("in none")
        #     return Response({"username":None})    
        

class Login(APIView):
    def post(self, request):
        username1 = request.data['username']
        password1 = request.data['password']
        user = authenticate(username = username1, password = password1)
        if user is None:
            return Response({"msg":None})
        else:    
            payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
            }
            token = jwt.encode(payload, 'secret', algorithm='HS256')
            #response = HttpResponse(status=200)
            #response.set_cookie(key='access_token', value="hello", max_age=3600, httponly=True, secure=True)
            #print("in httpres")
            # response.data = {
            #     'jwt': token
            #     #"username":user
            # }
            #return response
            return Response({"jwt":token})



class user_home(APIView):
    def get(self, request):
        token = request.GET.get('token_id')
        if not token:
            return Response({"msg":None})

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
            print(payload)
        except jwt.ExpiredSignatureError:
            return JsonResponse({"msg":None})

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class user_logout(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response



# def authendication(userid, request):
#     print(userid,"userid")
#     payload = {
#     'id': userid,
#     'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
#     'iat': datetime.datetime.utcnow()
#     }
#     token = jwt.encode(payload, 'secret', algorithm='HS256')
#     print(token)
#     response = Response()
#     response.set_cookie(key='jwt', value=token, httponly=True)
#     # response.data = {
#     #     'jwt': token
#     # }
#     return response

# def user_login(request):
#     return render(request,'user_login.html')

# def user_signup(request):
#     return render(request,'user_signup.html')    

# def user_logout(request):
#     return redirect('user_signup')