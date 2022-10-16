from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_page_view, name='main_page'),
    path('login/', views.user_login_view, name='login'),
    path('logout/', views.user_logout_view, name='logout'),
]
