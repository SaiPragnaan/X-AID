from django.shortcuts import render

# Create your views here.
def chatbot(request):
    return render(request,"chatbot_app/chatbot.html",{})

def disease_prediction(request):
    return render(request,"",{})

def login(request):
    return render(request,"",{})

def logout(request):
    return render(request,"",{})