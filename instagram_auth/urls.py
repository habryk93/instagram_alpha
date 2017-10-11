from django.conf.urls import url

from views import RegisterView
from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^register', RegisterView.as_view(), name='instagram.register'),
    url(r'^login$', auth_views.login, {'template_name': 'login.html'}, name='instagram.login'),
    url(r'^logout', auth_views.logout, name='instagram.logout')
]