from django.shortcuts import render , HttpResponse
from .models import todoitem

# Create your views here.


def home(request):
 return render(request,"main_code.html")

def todos(request):
 items=todoitem.objects.all()
 return render(request, "todos.html", {"todos": items})


