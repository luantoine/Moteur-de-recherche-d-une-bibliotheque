from django.urls import path
from .views import get_book
from django.http import JsonResponse

def test_route(request):
    return JsonResponse({"message": "API is working"})

urlpatterns = [
    path('test/', test_route, name='test_route'),
    path('book/<str:book_id>/', get_book, name='get_book'),
]