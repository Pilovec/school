from django.shortcuts import render
import requests, time
from bs4 import BeautifulSoup as bs
from datetime import date

def blog(request):
    headers = {'accept': '*/*',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
        }

    base_url = 'https://osvita.ua/school/news/'
    session = requests.Session()
    on_request = session.get(base_url, headers=headers)
    urls_list=[]
    if on_request.status_code == 200:
        soup = bs(on_request.content, 'lxml')
        posts = soup.find('table', attrs={'class':'list'}).find_all('tr')
        # current_date = date.today().strftime("%d.%m.%Y")
        current_date = '21.11.2019'
        description = ""
        for post in posts:
            if post.find('a') is not None:

                date_post = post.find('span', attrs={'class':'bdate'}).text
                if date_post == current_date:
                    title = post.find('a').text
                    title_link = post.find('a')['href']
                    short_descr = post.find('span', attrs={'class':'btxt'}).text
                    post_link = 'https://osvita.ua'+title_link
                    request_2 = session.get(post_link, headers=headers)
                    soup_2 = bs(request_2.content, 'lxml')
                    paragrafs = soup_2.find('article', attrs={'class':'article'}).find_all('p')
                    for p in paragrafs[:-2]:
                        description = description+(p.text)+"\n"
                    context = {
                        'title': title,
                        'title_link': title_link,
                        'short_descr': short_descr,
                        'description': description
                    }
            else:
                continue
    else:
        print('Error')
    return render(request, 'blog/blog.html', context)
