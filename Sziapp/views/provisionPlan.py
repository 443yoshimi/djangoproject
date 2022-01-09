from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
    
def szi_provisionP(request):
    
    return render(request,'provisionPlan.html')
