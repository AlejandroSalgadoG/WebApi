from django.shortcuts import render

def index(request):
    context = {
        "hello": "Hello",
    }
    return render(request, "index.html", context)