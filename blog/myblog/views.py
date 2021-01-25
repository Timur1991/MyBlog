from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.views import View
from .models import Post
from django.core.paginator import Paginator
from .forms import RegForm, AuthForm, FeedBackForm
from django.contrib.auth import login, authenticate
from django.http import HttpResponseRedirect, HttpResponse
from django.core.mail import send_mail, BadHeaderError

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
        return render(request, 'myblog/post_detail.html', context={'post': post})


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
                send_mail(f'От {name} | {subject}', message, from_email, ['amromashov@gmail.com'])
            except BadHeaderError:
                return HttpResponse('Невалидный заголовок')
            return HttpResponseRedirect('success')
        return render(request, 'myblog/contact.html',
                      context={'form': form})