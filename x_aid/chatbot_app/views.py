from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Chat
import json
import os

from django.utils import timezone
# Create your views here.
def chatbot(request):
    # chats=Chat.objects.filter(user=request.user)
    if request.method=="POST":
        data=json.loads(request.body)
        message=data.get("message")
        reply=f"You said: {message}"
        chat=Chat(user=request.user,message=message,response=reply,created_at=timezone.now())
        chat.save()
        return JsonResponse({"message":message,"reply": reply})
    # return render(request,"chatbot_app/chatbot.html",{'chats':chats})
    return render(request,"chatbot_app/chatbot.html",{})

def disease_prediction(request):
    return render(request,"",{})

def login(request):
    return render(request,"login.html",{})

def logout(request):
    auth.logout(request)
    return redirect("chatbot/")
    return render(request,"",{})