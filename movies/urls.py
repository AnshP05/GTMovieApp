from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('<int:pk>/', views.movie_detail, name='movie_detail'),

    # review routes
    path('<int:movie_id>/reviews/add/', views.review_create, name='review_create'),
    path('reviews/<int:pk>/edit/', views.review_edit, name='review_edit'),
    path('reviews/<int:pk>/delete/', views.review_delete, name='review_delete'),

    # 🔍 search route
    path('search/', views.search, name='search'),
]
