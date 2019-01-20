from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request,'goods/index.html')
def category(request):
    return render(request,'goods/category.html')