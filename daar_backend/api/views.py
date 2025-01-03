from django.shortcuts import render
from django.http import JsonResponse
from pymongo import MongoClient
from django.conf import settings
from .services.mongo_client import MongoDBClient

# test
def get_book(request, book_id):
    """
    Récupère un livre par son ID depuis la base MongoDB
    """
    try:
        mongo_client = MongoDBClient()
        collection = mongo_client.get_collection("gutenberg_books")
        
        book = collection.find_one({"book_id": book_id})
        
        if book:
            book['_id'] = str(book['_id'])
            return JsonResponse(book)
        else:
            return JsonResponse({"error": "Book not found"}, status=404)
    except Exception as e:
        return JsonResponse({"error": f"Internal server error: {str(e)}"}, status=500)