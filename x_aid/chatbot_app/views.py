from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Chat
import json
import os

import sys
sys.path.append('/home/unique/Dev/X-AID/ML/')


from scripts.chat_generation import text_generation

from django.utils import timezone
# Create your views here.

def chatbot(request):
    chats=Chat.objects.filter(user=request.user)
    if request.method=="POST":
        if request.FILES.get("image"):
            image = request.FILES["image"]

            bot_reply = "I received your image. Processing..."
            bot_image = None  

            chat = Chat(user=request.user, image=image,response=bot_reply ,bot_image=bot_image,created_at=timezone.now())
            chat.save()
            return JsonResponse({
                "bot_reply": bot_reply,
                "bot_image": bot_image.url if bot_image else None
            })

        elif request.body:
            data = json.loads(request.body)
            query = data.get("message")
            reply = text_generation(query)
            # reply="processinggggggggggg"
            
            chat = Chat(user=request.user, message=query, response=reply, created_at=timezone.now())
            chat.save()

            return JsonResponse({"message": query, "reply": reply})
    
    return render(request,"chatbot_app/chatbot.html",{'chats':chats})

def disease_prediction(request):
    return render(request,"",{})

def login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if not username or not password:
            return render(request, "chatbot_app/login.html", {"error_message": "All fields are required."})
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('chatbot')
        else:
            error_message = "Invalid username or password."
            return render(request,'chatbot_app/login.html',{'error_message':error_message})

    return render(request,"chatbot_app/login.html",{})

def register(request):
    if request.method == "POST":
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']

        if password1 == password2:
            try:
                user=User.objects.create_user(username=username, email=email,password=password1)
                user.save()
                auth.login(request,user)
                return redirect('chatbot')
            except:
                error_message="Error Creating account"
                return render(request,'register.html',{'error_message':error_message})
        else:
            error_message="Passwords don't match"
            return render(request,'register.html',{'error_message':error_message})

    return render(request,'chatbot_app/register.html')

def logout(request):
    auth.logout(request)
    return redirect("chatbot/")