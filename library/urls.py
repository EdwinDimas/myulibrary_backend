from django.urls import path
from .views import ( create_books, list_authors, list_books, find_books, list_genres, update_book_stock,
    make_request, create_status_detail, create_user )

urlpatterns = [
    path('books/create/', create_books, name='create_books'),
    path('books/', list_books, name='list_books'),
    path('books/genres', list_genres, name='list_genres'),
    path('books/authors', list_authors, name='list_authors'),
    path('books/search/', find_books, name='find_books'),
    path('books/<int:book_id>/update_stock/', update_book_stock, name='update_book_stock'),
    path('requests/create/', make_request, name='make_request'),
    path('status_details/create/', create_status_detail, name='create_status_detail'),
    path('users/create/', create_user, name='create_user'),
]