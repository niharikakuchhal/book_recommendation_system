from django.urls import path
from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
     path('search/', search_book, name='search_book'),
    path('recommendations/', book_recommendation, name='book_recommendation'),
    path('recommendations/add/', recommend_book_form, name='recommend_book_form'),
    path('recommendations/my/', view_recommendations, name='view_recommendations'),
    path('recommendations/all/', recommended_books, name='recommended_books'),
    path('recommendations/like/', like_recommendation, name='like_recommendation'),
    path('recommendations/comment/<int:recommendation_id>/', add_comment, name='add_comment'),
    path('recommendations/add_to_recommendations/', add_to_recommendations, name='add_to_recommendations'),
]
