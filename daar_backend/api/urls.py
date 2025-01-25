from django.urls import path
from .views import get_book, search_books,advanced_search_books, kmp_search_books, automate_regex_search_books, get_books_by_centrality
from django.http import JsonResponse

def test_route(request):
    return JsonResponse({"message": "API is working"})

urlpatterns = [
    path('test/', test_route, name='test_route'),
    path('book/<str:book_id>/', get_book, name='get_book'),
    path('search/', search_books, name='search_books'), 
    path('advanced_search/', advanced_search_books, name='advanced_search_books'),
    path('search/kmp/', kmp_search_books, name='kmp_search_books'),
    path('search/automate/', automate_regex_search_books, name='automate_regex_search'),
    path('get-books-centrality/', get_books_by_centrality, name='get_books_centrality'),
]