from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
import requests, time
from bs4 import BeautifulSoup as bs
from datetime import date
from .models import Source, Post


def post_list(request):
    if request.method == 'POST':
        headers = {'accept': '*/*',
                        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
                    }
        base_url = 'https://osvita.ua/school/news/'
        session = requests.Session()
        on_request = session.get(base_url, headers=headers)
        urls_list=[]
        if on_request.status_code == 200:

            soup = bs(on_request.content, 'lxml')
            news = soup.find('table', attrs={'class':'list'}).find_all('tr')
            # current_date = date.today().strftime("%d.%m.%Y")
            current_date = '6.12.2019'
            for news_item in news:

                if news_item.find('a') is not None:
                    date_post = news_item.find('span', attrs={'class':'bdate'}).text
                    if date_post.lstrip(' ') == current_date:
                        img = news_item.find('img', attrs={'class':'h92'})['src']
                        title = news_item.find('a').text
                        title_link = news_item.find('a')['href']
                        short_descr = news_item.find('span', attrs={'class':'btxt'}).text
                        post_link = 'https://osvita.ua'+title_link
                        add = Post()
                        add.title = title
                        add.photo_main = 'https:' + img
                        add.post_link = post_link
                        add.short_description = short_descr
                        add.source = Source.objects.filter(name='osvita.ua').first()
                        add.save()
                    else:
                        continue
                else:
                    continue

            return redirect('post_list')
    posts = Post.objects.order_by('-pub_date')
    paginator = Paginator(posts, 6)
    page = request.GET.get('page')
    paged_posts = paginator.get_page(page)
    context = {
        'posts': paged_posts
    }
    return render(request, 'blog/post_list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    # text = post.description.split("#")
    context = {
        'post': post
        # 'text': text
    }
    return render(request, 'blog/post_detail.html', context)



# def post_list(request):
#     if request.method == 'POST':
#         headers = {'accept': '*/*',
#                 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
#             }
#
#         base_url = 'https://osvita.ua/school/news/'
#
#         session = requests.Session()
#         on_request = session.get(base_url, headers=headers)
#         urls_list=[]
#         if on_request.status_code == 200:
#             soup = bs(on_request.content, 'lxml')
#             posts = soup.find('table', attrs={'class':'list'}).find_all('tr')
#             # current_date = date.today().strftime("%d.%m.%Y")
#             current_date = '21.11.2019'
#             print(current_date)
#             description = ""
#             for post in posts:
#                 if post.find('a') is not None:
#
#                     date_post = post.find('span', attrs={'class':'bdate'}).text
#                     if date_post == current_date:
#                         title = post.find('a').text
#                         title_link = post.find('a')['href']
#                         short_descr = post.find('span', attrs={'class':'btxt'}).text
#                         post_link = 'https://osvita.ua'+title_link
#                         request_2 = session.get(post_link, headers=headers)
#                         soup_2 = bs(request_2.content, 'lxml')
#                         paragrafs = soup_2.find('article', attrs={'class':'article'}).find_all('p')
#                         for p in paragrafs[:-2]:
#                             description = description+(p.text)+"\n"
#                         Post().title = title
#                         Post().short_description = short_descr
#                         Post().description = description
#                         Post().source = Source.objects.filter(slug='admin')
#                         Post().save()
#                         return redirect('blog')
#                 else:
#                     continue
#         else:
#             print('Error')
#     else:
#         posts = Post.objects.order_by('-pub_date')
#         context = {
#             'posts': posts
#         }
#         return render(request, 'blog/post_list.html', context)
