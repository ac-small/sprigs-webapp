from django.urls import path

from . import views

app_name = 'sprigs'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category/', views.run, name='run'),
]
