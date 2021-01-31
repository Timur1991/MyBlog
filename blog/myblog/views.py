# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import View
# импорт нашей модели
from .models import Post
# импорт пагинатора
from django.core.paginator import Paginator
# импорт наших форм
from .forms import RegForm, AuthForm, FeedBackForm
# импорт авторизации
from django.contrib.auth import login, authenticate
# импорт для отправки писем на почту
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail, BadHeaderError
# испорт для работы с тэгами
from taggit.models import Tag

# без пагинации
# class MainView(View):
#     def get(self, request, *args, **kwargs):
#         posts = Post.objects.all()
#         return render(request, 'myblog/index.html', context={'posts': posts})


#  спагинацией
class MainView(View):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        paginator = Paginator(posts, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'myblog/index.html', context={'page_obj': page_obj})


class PostDetailView(View):
    def get(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, url=slug)
        # добавим отображение тэгов и последних постов
        common_tags = Post.tag.most_common()
        last_posts = Post.objects.all().order_by('-id')[:5]
        return render(request, 'myblog/post_detail.html', context={
            'post': post,
            'common_tags': common_tags,
            'last_posts': last_posts
        })


class RegView(View):
    def get(self, request, *args, **kwargs):
        form = RegForm()
        return render(request, 'myblog/reg.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = RegForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'myblog/reg.html', context={
            'form': form,
        })


class AuthView(View):
    def get(self, request, *args, **kwargs):
        form = AuthForm()
        return render(request, 'myblog/auth.html', context={
            'form': form,
        })

    def post(self, request, *args, **kwargs):
        form = AuthForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/')
        return render(request, 'myblog/auth.html', context={
            'form': form,
        })


class FeedBackView(View):
    def get(self, request, *args, **kwargs):
        form = FeedBackForm()
        return render(request, 'myblog/contact.html',
                      context={'form': form, 'title': 'Написать мне'})

    def post(self, request, *args, **kwargs):
        form = FeedBackForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            from_email = form.cleaned_data['email']
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            try:
                send_mail(f'От {name}[{from_email}] | {subject}', message, from_email, ['lltima1991ll@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Невалидный заголовок')
            return HttpResponseRedirect('success')
        return render(request, 'myblog/contact.html',
                      context={'form': form})


class SuccessView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'myblog/success.html', context={'title': 'Спасибо'})

from django.db.models import Q


# class SearchResultView(View):
#     """Поиск без пагинации"""
#     def get(self, request, *args, **kwargs):
#         query = self.request.GET.get('q')
#         results = ''
#         if query:
#             results = Post.objects.filter(
#                 Q(h1__icontains=query) | Q(content__icontains=query)
#             )
#         return render(request, 'myblog/search.html', context={
#             'title': 'Поиск',
#             'results': results,
#             'count': len(results)
#                       })


class SearchResultView(View):
    """Поиск с пагинацией"""
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('q')
        results = ''
        if query:
            results = Post.objects.filter(
                Q(h1__icontains=query) | Q(content__icontains=query)
            )
        # создаем пагинацию, по 6 результатов на странице
        paginator = Paginator(results, 6)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'myblog/search.html', context={
            'title': 'Поиск',
            'results': page_obj,
            'count': paginator.count
                      })


class TagView(View):
    def get(self, request, slug, *args, **kwargs):
        tag = get_object_or_404(Tag, slug=slug)
        posts = Post.objects.filter(tag=tag)
        common_tags = Post.tag.most_common()
        return render(request, 'myblog/tag.html', context={
            'title': f'#ТЕГ {tag}',
            'posts': posts,
            'common_tags': common_tags
        })