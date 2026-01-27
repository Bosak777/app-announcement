from django.shortcuts import render

# Create your views here.


def home(request):
    return render(request, "home/home.html")


def yonmoku_title(request):
    return render(request, "home/yonmoku_title.html")
