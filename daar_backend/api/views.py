# daar_backend/api/views.py

from django.http import JsonResponse
from django.views.decorators.http import require_GET
from .services.mongo_client import mongo_client
import re
from bson import ObjectId
import logging

# Configuration du logger
logger = logging.getLogger('api')  # Assurez-vous que le nom correspond à votre configuration de logging

def convert_objectid(doc):
    """
    Convertit le champ '_id' de type ObjectId en chaîne de caractères.
    """
    if '_id' in doc and isinstance(doc['_id'], ObjectId):
        doc['_id'] = str(doc['_id'])
    return doc

def get_suggestions(top_results, collection, max_suggestions=10):
    """
    Génère des suggestions basées sur les voisins dans le graphe de Jaccard des documents principaux.
    
    Args:
        top_results (list): Liste des documents principaux (les plus pertinents).
        collection (Collection): Collection MongoDB.
        max_suggestions (int): Nombre maximum de suggestions à retourner.
    
    Returns:
        list: Liste des documents suggérés.
    """
    try:
        neighbor_ids = set()
        for doc in top_results[:3]:  # Considérer les trois premiers documents
            neighbors = doc.get("neighbors", [])
            neighbor_ids.update(neighbors)
        
        # Exclure les IDs des documents déjà dans les résultats principaux
        top_ids = set(doc.get("book_id") for doc in top_results[:3])
        neighbor_ids = neighbor_ids - top_ids
        
        if not neighbor_ids:
            return []
        
        # Limiter le nombre de suggestions
        neighbor_ids = list(neighbor_ids)[:max_suggestions]
        
        # Rechercher les documents correspondants aux voisins
        suggestions_cursor = collection.find({"book_id": {"$in": neighbor_ids}})
        
        suggestions = []
        for sugg in suggestions_cursor:
            sugg = convert_objectid(sugg)
            # Simplifier la structure si nécessaire
            sugg["authors"] = [author["name"] for author in sugg.get("authors", [])]
            suggestions.append(sugg)
        
        return suggestions
    except Exception as e:
        logger.error(f"Erreur lors de la génération des suggestions: {e}")
        return []

@require_GET
def get_book(request, book_id):
    """
    Récupère un livre par son ID depuis la base MongoDB.
    """
    try:
        # Valider que book_id est composé uniquement de chiffres
        if not re.match(r'^\d+$', book_id):
            return JsonResponse({"error": "Format de book_id invalide."}, status=400)

        collection = mongo_client.get_collection("gutenberg_books")
        
        # Rechercher le livre par book_id
        book = collection.find_one({"book_id": book_id})
        
        if book:
            # Convertir ObjectId en chaîne de caractères
            book = convert_objectid(book)
            # Simplifier la structure si nécessaire
            book["authors"] = [author["name"] for author in book.get("authors", [])]
            return JsonResponse(book, safe=False)
        else:
            return JsonResponse({"error": "Livre non trouvé."}, status=404)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du livre ID={book_id}: {e}")
        return JsonResponse({"error": f"Erreur interne du serveur : {str(e)}"}, status=500)

@require_GET
def search_books(request):
    """
    Recherche de livres par mot-clé sur les champs "title", "authors.name" et "text".
    Renvoie l'intégralité du document triée par pertinence et des suggestions similaires.
    """
    try:
        # Récupérer le paramètre de recherche 'q'
        query = request.GET.get('q', '').strip()
        if not query:
            return JsonResponse({"error": "Aucun mot-clé fourni pour la recherche."}, status=400)
        
        # Optionnel : Limiter la longueur de la requête pour des raisons de sécurité
        if len(query) > 100:
            return JsonResponse({"error": "La requête est trop longue."}, status=400)
        
        # Connexion à la collection MongoDB
        collection = mongo_client.get_collection("gutenberg_books")
        
        # Rechercher dans les champs indexés "title", "authors.name" et "text"
        cursor = collection.find(
            { "$text": { "$search": query } }
        ).limit(100)  # Limiter les résultats pour la performance
        
        results = []
        for book in cursor:
            # Compter les occurrences du mot-clé dans le champ 'text'
            text = book.get("text", "")
            occurrences = len(re.findall(re.escape(query), text, re.IGNORECASE))
            
            # Récupérer l'indice de centralité
            centrality = book.get("centrality", 0)
            
            # Ajouter les critères de classement
            book["occurrences"] = occurrences
            book["centrality"] = centrality
            
            # Convertir ObjectId en chaîne de caractères
            book = convert_objectid(book)
            
            results.append(book)
        
        # Classer les résultats par occurrences (desc) puis centralité (desc)
        sorted_results = sorted(results, key=lambda x: (x["occurrences"], x["centrality"]), reverse=True)
        
        # Obtenir les suggestions basées sur les top 3 résultats
        suggestions = get_suggestions(sorted_results, collection)
        
        return JsonResponse({"results": sorted_results, "suggestions": suggestions}, status=200)
    
    except Exception as e:
        logger.error(f"Erreur lors de la recherche de livres avec query='{query}': {e}")
        return JsonResponse({"error": f"Erreur interne du serveur : {str(e)}"}, status=500)

@require_GET
def advanced_search_books(request):
    """
    Recherche avancée de livres en utilisant des expressions régulières (RegEx) sur les champs "title", "authors.name" et "text".
    Renvoie l'intégralité du document triée par pertinence et des suggestions similaires.
    """
    try:
        # Récupérer les paramètres de recherche
        regex_pattern = request.GET.get('regex', '').strip()
        limit = int(request.GET.get('limit', 100))
        offset = int(request.GET.get('offset', 0))
        
        if not regex_pattern:
            return JsonResponse({"error": "Aucune expression régulière fournie pour la recherche avancée."}, status=400)
        
        # Limiter la longueur de la requête pour des raisons de sécurité
        if len(regex_pattern) > 200:
            return JsonResponse({"error": "L'expression régulière est trop longue."}, status=400)
        
        # Valider que l'expression régulière est valide
        try:
            re.compile(regex_pattern)
        except re.error:
            return JsonResponse({"error": "Expression régulière invalide."}, status=400)
        
        # Connexion à la collection MongoDB
        collection = mongo_client.get_collection("gutenberg_books")
        
        # Déterminer les champs à rechercher avec RegEx
        search_fields = ["title", "authors.name", "text"]
        
        # Construire la requête RegEx pour les champs d'indexage
        regex_queries = [{field: {"$regex": regex_pattern, "$options": "i"}} for field in search_fields]
        
        # Construire la requête finale avec $or
        mongo_query = {"$or": regex_queries}
        
        # Exécuter la requête RegEx avec pagination
        cursor = collection.find(mongo_query).skip(offset).limit(limit)
        
        results = []
        for book in cursor:
            # Compter les occurrences du mot-clé dans le champ 'text' en utilisant le pattern RegEx
            text = book.get("text", "")
            occurrences = len(re.findall(regex_pattern, text, re.IGNORECASE))
            
            # Récupérer l'indice de centralité
            centrality = book.get("centrality", 0)
            
            # Ajouter les critères de classement
            book["occurrences"] = occurrences
            book["centrality"] = centrality
            
            # Convertir ObjectId en chaîne de caractères
            book = convert_objectid(book)
            
            results.append(book)
        
        # Classer les résultats par occurrences (desc) puis centralité (desc)
        sorted_results = sorted(results, key=lambda x: (x["occurrences"], x["centrality"]), reverse=True)
        
        # Obtenir les suggestions basées sur les top 3 résultats
        suggestions = get_suggestions(sorted_results, collection)
        
        return JsonResponse({"results": sorted_results, "suggestions": suggestions}, status=200)
    
    except Exception as e:
        logger.error(f"Erreur lors de la recherche avancée avec regex='{regex_pattern}': {e}")
        return JsonResponse({"error": f"Erreur interne du serveur : {str(e)}"}, status=500)
