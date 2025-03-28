from django.http import JsonResponse
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from .models import Chat
import json
import os

# Create your views here.
def chatbot(request):
    chats=Chat.objects.filter(user=request.user)
    if request.method=="POST":
        data=json.loads(request.body)
        message=data.get("message")
        # return JsonResponse({"message":message,"response": response})
        return JsonResponse({"reply": f"You said: {message}"})
    return render(request,"chatbot_app/chatbot.html",{'chats':chats})

def disease_prediction(request):
    return render(request,"",{})

def login(request):
    return render(request,"",{})

def logout(request):
    return render(request,"",{})