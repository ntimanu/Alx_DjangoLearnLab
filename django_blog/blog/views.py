from django.shortcuts import render
from .models import Post

def home(request):
    return render(request, 'blog/base.html')

def posts(request):
    posts = Post.objects.all().order_by('-published_date')
    return render(request, 'blog/posts.html', {'posts': posts})

def login_view(request):
    return render(request, 'blog/login.html')

def register_view(request):
    return render(request, 'blog/register.html')