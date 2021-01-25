from django.urls import path
from .views import MainView, PostDetailView, RegView, AuthView
from django.contrib.auth.views import LogoutView
from django.conf import settings

urlpatterns = [
    path('', MainView.as_view(), name='index'),
    path('blog/<slug>/', PostDetailView.as_view(), name='post_detail'),
    path('reg/', RegView.as_view(), name='reg'),
    path('auth/', AuthView.as_view(), name='auth'),
    path('out/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='out'),

]