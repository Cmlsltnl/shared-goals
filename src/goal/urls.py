from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.GoalView.as_view(), name='index'),
    url(r'^profile/$', views.ProfileView.as_view(), name='profile'),
]
