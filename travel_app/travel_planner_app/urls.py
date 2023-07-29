from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup, name='signup'),
    path('input/', views.input_page, name='input'),
    path('output/', views.output_page, name='output'),
    path('automated/', views.automated_plan, name='automated'),
    path('customized/', views.customized_plan, name='customized'),
    path('trip-with-strangers/', views.trip_with_strangers, name='trip_with_strangers'),
    path('feedback/', views.feedback, name='feedback'),
]