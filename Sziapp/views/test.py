from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse('Hello')
    
def index_template(request):
    return render(request,'TEST/test.html')
