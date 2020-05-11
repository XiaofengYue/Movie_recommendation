from django.urls import path,include
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /movies/5/
    path('<int:movie_id>/', views.detail, name='detail'),
    # ex: /movies/5/rate
    path('<int:movie_id>/rate', views.rate, name='rate'),

    path('login/', views.login, name='login'),

    path('logout/', views.logout, name='logout'),

    path('register/', views.register, name='register'),

    path('search', views.search, name='search'),

    path('user/<str:user_id>', views.user, name='user'),

    path('rec', views.rec, name='rec'),
]

