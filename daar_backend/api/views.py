from django.shortcuts import render
from django.http import JsonResponse

def api_search(request):
    query = request.GET.get('query', '')
    # TODO: à remplacer par appel backend 
    results = ["Book 1", "Book 2", "Book 3"]
    return JsonResponse({'query': query, 'results': results})