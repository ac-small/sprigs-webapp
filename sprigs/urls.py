from django.urls import path

from . import views

app_name = 'sprigs'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('category/', views.OrderListJson.as_view(), name='order_list_json'),
    #path('category/result', views.ResultsView.as_view(), name='order_list_json'),

]
