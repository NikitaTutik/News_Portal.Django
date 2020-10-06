import json
from django.views import View
from django.http.response import HttpResponse
from django.conf import settings
from django.shortcuts import render, redirect
import itertools
import random
from datetime import datetime
from django.template.defaulttags import register


# Create your tests here.


class WelcomeView(View):
    def get(self, request, *args, **kwargs):
        return redirect('/news/')


class ViewNews(View):
    def get(self, request, post_id, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            json_dict = json.load(json_file)
            for i in json_dict:
                if post_id == i['link']:
                    new = i
            context = {'new': new}
            return render(request, 'news/news.html', context)


class MainNews(View):
    def get(self, request, *args, **kwargs):
        with open(settings.NEWS_JSON_PATH, 'r') as json_file:
            news_list = json.load(json_file)
        def myFunc(e):
            return e['created']
        news_list.sort(reverse=True, key=myFunc)
        context = {
                'news_list': news_list,
        }
        query = str(request.GET.get('q'))
        for i in news_list:
            if query in i['title']:
                context = {
                    'news_list': [i]
                }
        return render(request, 'news/all_news.html', context)



class CreateNews(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'news/create.html')

    def post(self, request, *args, **kwargs):
        def random_link():
            link_list = []
            with open(settings.NEWS_JSON_PATH, 'r') as json_file:
                news_list = json.load(json_file)
                for i in news_list:
                    link_list.append(i['link'])
                n = random.getrandbits(32)
                if n in link_list:
                    n = random.getrandbits(32)
                else:
                    return n
        created = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        news_dict = {
            'created': str(created),
            'text': request.POST.get('text'),
            'title': request.POST.get('title'),
            'link': random_link()
        }
        with open(settings.NEWS_JSON_PATH) as f:
            data = json.load(f)
        data.append(news_dict)
        with open(settings.NEWS_JSON_PATH, 'w') as f:
            json.dump(data, f)
        return redirect('/news/')

