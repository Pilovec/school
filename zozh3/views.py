from django.shortcuts import render
from blog.models import Post, Source

def index(request):
    posts = Post.objects.order_by('-pub_date')[:6]
    context = {
        'posts': posts
    }
    return render(request, 'zozh3/index.html', context)
