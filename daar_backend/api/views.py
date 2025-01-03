from django.shortcuts import render
from django.http import JsonResponse
from .mongo_client import mongo_client

def api_search(request):
    query = request.GET.get('query', '')

    # Accéder à la collection "books"
    books_collection = mongo_client.get_collection('books')

    # TODO: modifier avec les algo
    results = books_collection.find({'content': {'$regex': query, '$options': 'i'}})

    # Convertir les résultats en une liste de dictionnaires
    books = [{'title': book['title'], 'author': book['author']} for book in results]

    return JsonResponse({'query': query, 'results': books})

# test
def test_mongo_connection(request):
    books_collection = mongo_client.get_collection('books')
    count = books_collection.count_documents({})
    return JsonResponse({'message': 'Connected successfully', 'books_count': count})