# daar_backend/api/views.py

from django.http import JsonResponse
from django.views.decorators.http import require_GET
import re
import logging
from django.db import connection
from api.algorithms.kmp import compute_lps, kmp_search_pos
from api.algorithms.automate import search_regex, minimize_dfa, ndfa_to_dfa, to_ndfa, parse
from django.views.decorators.cache import cache_page

# Configuration du logger
logger = logging.getLogger('api')  # Assurez-vous que le nom correspond à votre configuration de logging

# def convert_objectid(doc):
#     """
#     Convertit le champ '_id' de type ObjectId en chaîne de caractères.
#     """
#     if '_id' in doc and isinstance(doc['_id'], ObjectId):
#         doc['_id'] = str(doc['_id'])
#     return doc

# def get_suggestions(top_results, collection, max_suggestions=10):
#     """
#     Génère des suggestions basées sur les voisins dans le graphe de Jaccard des documents principaux.
    
#     Args:
#         top_results (list): Liste des documents principaux (les plus pertinents).
#         collection (Collection): Collection MongoDB.
#         max_suggestions (int): Nombre maximum de suggestions à retourner.
    
#     Returns:
#         list: Liste des documents suggérés.
#     """
#     try:
#         neighbor_ids = set()
#         for doc in top_results[:3]:  # Considérer les trois premiers documents
#             neighbors = doc.get("neighbors", [])
#             neighbor_ids.update(neighbors)
        
#         # Exclure les IDs des documents déjà dans les résultats principaux
#         top_ids = set(doc.get("book_id") for doc in top_results[:3])
#         neighbor_ids = neighbor_ids - top_ids
        
#         if not neighbor_ids:
#             return []
        
#         # Limiter le nombre de suggestions
#         neighbor_ids = list(neighbor_ids)[:max_suggestions]
        
#         # Rechercher les documents correspondants aux voisins
#         suggestions_cursor = collection.find({"book_id": {"$in": neighbor_ids}})
        
#         suggestions = []
#         for sugg in suggestions_cursor:
#             sugg = convert_objectid(sugg)
#             # Simplifier la structure si nécessaire
#             sugg["authors"] = [author["name"] for author in sugg.get("authors", [])]
#             suggestions.append(sugg)
        
#         return suggestions
#     except Exception as e:
#         logger.error(f"Erreur lors de la génération des suggestions: {e}")
#         return []

# @require_GET
# def get_book(request, book_id):
#     """
#     Récupère un livre par son ID depuis la base MongoDB.
#     """
#     try:
#         # Valider que book_id est composé uniquement de chiffres
#         if not re.match(r'^\d+$', book_id):
#             return JsonResponse({"error": "Format de book_id invalide."}, status=400)

#         collection = mongo_client.get_collection("gutenberg_books")
        
#         # Rechercher le livre par book_id
#         book = collection.find_one({"book_id": book_id})
        
#         if book:
#             # Convertir ObjectId en chaîne de caractères
#             book = convert_objectid(book)
#             # Simplifier la structure si nécessaire
#             book["authors"] = [author["name"] for author in book.get("authors", [])]
#             return JsonResponse(book, safe=False)
#         else:
#             return JsonResponse({"error": "Livre non trouvé."}, status=404)
#     except Exception as e:
#         logger.error(f"Erreur lors de la récupération du livre ID={book_id}: {e}")
#         return JsonResponse({"error": f"Erreur interne du serveur : {str(e)}"}, status=500)

# @require_GET
# def search_books(request):
#     """
#     Recherche de livres par mot-clé sur les champs "title", "authors.name" et "text".
#     Renvoie l'intégralité du document triée par pertinence et des suggestions similaires.
#     """
#     try:
#         # Récupérer le paramètre de recherche 'q'
#         query = request.GET.get('q', '').strip()
#         if not query:
#             return JsonResponse({"error": "Aucun mot-clé fourni pour la recherche."}, status=400)
        
#         # Optionnel : Limiter la longueur de la requête pour des raisons de sécurité
#         if len(query) > 100:
#             return JsonResponse({"error": "La requête est trop longue."}, status=400)
        
#         # Connexion à la collection MongoDB
#         collection = mongo_client.get_collection("gutenberg_books")
        
#         # Rechercher dans les champs indexés "title", "authors.name" et "text"
#         cursor = collection.find(
#             { "$text": { "$search": query } }
#         ).limit(100)  # Limiter les résultats pour la performance
        
#         results = []
#         for book in cursor:
#             # Compter les occurrences du mot-clé dans le champ 'text'
#             text = book.get("text", "")
#             occurrences = len(re.findall(re.escape(query), text, re.IGNORECASE))
            
#             # Récupérer l'indice de centralité
#             centrality = book.get("centrality", 0)
            
#             # Ajouter les critères de classement
#             book["occurrences"] = occurrences
#             book["centrality"] = centrality
            
#             # Convertir ObjectId en chaîne de caractères
#             book = convert_objectid(book)
            
#             results.append(book)
        
#         # Classer les résultats par occurrences (desc) puis centralité (desc)
#         sorted_results = sorted(results, key=lambda x: (x["occurrences"], x["centrality"]), reverse=True)
        
#         # Obtenir les suggestions basées sur les top 3 résultats
#         suggestions = get_suggestions(sorted_results, collection)
        
#         return JsonResponse({"results": sorted_results, "suggestions": suggestions}, status=200)
    
#     except Exception as e:
#         logger.error(f"Erreur lors de la recherche de livres avec query='{query}': {e}")
#         return JsonResponse({"error": f"Erreur interne du serveur : {str(e)}"}, status=500)

# @require_GET
# def advanced_search_books(request):
#     """
#     Recherche avancée de livres en utilisant des expressions régulières (RegEx) sur les champs "title", "authors.name" et "text".
#     Renvoie l'intégralité du document triée par pertinence et des suggestions similaires.
#     """
#     try:
#         # Récupérer les paramètres de recherche
#         regex_pattern = request.GET.get('regex', '').strip()
#         limit = int(request.GET.get('limit', 100))
#         offset = int(request.GET.get('offset', 0))
        
#         if not regex_pattern:
#             return JsonResponse({"error": "Aucune expression régulière fournie pour la recherche avancée."}, status=400)
        
#         # Limiter la longueur de la requête pour des raisons de sécurité
#         if len(regex_pattern) > 200:
#             return JsonResponse({"error": "L'expression régulière est trop longue."}, status=400)
        
#         # Valider que l'expression régulière est valide
#         try:
#             re.compile(regex_pattern)
#         except re.error:
#             return JsonResponse({"error": "Expression régulière invalide."}, status=400)
        
#         # Connexion à la collection MongoDB
#         collection = mongo_client.get_collection("gutenberg_books")
        
#         # Déterminer les champs à rechercher avec RegEx
#         search_fields = ["title", "authors.name", "text"]
        
#         # Construire la requête RegEx pour les champs d'indexage
#         regex_queries = [{field: {"$regex": regex_pattern, "$options": "i"}} for field in search_fields]
        
#         # Construire la requête finale avec $or
#         mongo_query = {"$or": regex_queries}
        
#         # Exécuter la requête RegEx avec pagination
#         cursor = collection.find(mongo_query).skip(offset).limit(limit)
        
#         results = []
#         for book in cursor:
#             # Compter les occurrences du mot-clé dans le champ 'text' en utilisant le pattern RegEx
#             text = book.get("text", "")
#             occurrences = len(re.findall(regex_pattern, text, re.IGNORECASE))
            
#             # Récupérer l'indice de centralité
#             centrality = book.get("centrality", 0)
            
#             # Ajouter les critères de classement
#             book["occurrences"] = occurrences
#             book["centrality"] = centrality
            
#             # Convertir ObjectId en chaîne de caractères
#             book = convert_objectid(book)
            
#             results.append(book)
        
#         # Classer les résultats par occurrences (desc) puis centralité (desc)
#         sorted_results = sorted(results, key=lambda x: (x["occurrences"], x["centrality"]), reverse=True)
        
#         # Obtenir les suggestions basées sur les top 3 résultats
#         suggestions = get_suggestions(sorted_results, collection)
        
#         return JsonResponse({"results": sorted_results, "suggestions": suggestions}, status=200)
    
#     except Exception as e:
#         logger.error(f"Erreur lors de la recherche avancée avec regex='{regex_pattern}': {e}")
#         return JsonResponse({"error": f"Erreur interne du serveur : {str(e)}"}, status=500)


################ PostgreSQL

def execute_sql_query(query, params=None):
    """
    Fonction pour exécuter une requête SQL brute
    Retourne les résultats sous forme de liste de dictionnaires
    """
    with connection.cursor() as cursor:
        cursor.execute(query, params or [])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

@require_GET
def get_book(request, book_id):
    """
    Récupérer un livre à partir de son ID
    """
    try:
        # Vérifier que l'ID est un entier valide
        if not re.match(r'^\d+$', book_id):
            return JsonResponse({"error": "Format de book_id invalide"}, status=400)

        # Requête SQL pour récupérer les infos du livre
        query = "SELECT * FROM books WHERE id = %s;"
        book = execute_sql_query(query, [book_id])
        
        if book:
            # Retourner les infos du premier résultat (s'il existe)
            book = book[0]
            return JsonResponse(book, safe=False)
        else:
            return JsonResponse({"error": "Livre non trouvé"}, status=404)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération du livre ID={book_id}: {e}")
        return JsonResponse({"error": f"Erreur interne du serveur : {str(e)}"}, status=500)

@require_GET
def search_books(request):
    """
    Recherche de livres par mot-clé
    On cherche dans les champs title, authors et text_content, et on classe par pertinence
    """
    try:
        # Récupérer le mot-clé de recherche
        query = request.GET.get('q', '').strip()
        if not query:
            return JsonResponse({"error": "Aucun mot-clé fourni pour la recherche"}, status=400)
        
        # Limiter la longueur de la requête pour éviter des abus
        if len(query) > 100:
            return JsonResponse({"error": "La requête est trop longue"}, status=400)

        # request body
        limit = int(request.GET.get('limit', 10)) # limite de livre 
        offset = int(request.GET.get('offset', 0)) # l'offset pour les pages
        sort_by = request.GET.get('sort', '') # criètre de tri

        # Requête pour rechercher par pertinence (utilise un index textuel)
        sql_query = """
        SELECT id, title, text_content,
            ts_rank_cd(search_content, plainto_tsquery('english', %s)) AS rank, centrality
        FROM books
        WHERE search_content @@ plainto_tsquery('english', %s)
        """
        results = execute_sql_query(sql_query, [query, query])
        
        for book in results:
            text = book.get('text_content', '') or ""
            occurrences = len(re.findall(re.escape(query), text, re.IGNORECASE))
            book['total_occurrences'] = occurrences

        if sort_by == 'centrality':
            results.sort(key=lambda b: (-b['rank'], -b['centrality'])) # Tri par centralité
            
        else:
            results.sort(key=lambda b: -b['total_occurrences'])  # Tri par fréquence décroissante 

        # Générer des suggestions basées sur les voisins du graphe
        suggestions = get_suggestions(results)
        

        page_result = results[offset:offset+limit]
        return JsonResponse({"results": page_result, "suggestions": suggestions}, status=200)
    except Exception as e:
        logger.error(f"Erreur lors de la recherche de livres avec query='{query}': {e}")
        return JsonResponse({"error": f"Erreur interne du serveur : {str(e)}"}, status=500)

@require_GET
def advanced_search_books(request):
    """
    Recherche avancée en utilisant des expressions régulières
    """
    try:
        # Récupérer les paramètres
        regex_pattern = request.GET.get('regex', '').strip()
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        if not regex_pattern:
            return JsonResponse({"error": "Aucune expression régulière fournie"}, status=400)
        
        if len(regex_pattern) > 200:
            return JsonResponse({"error": "L'expression régulière est trop longue"}, status=400)
        
        # Vérifier que l'expression régulière est valide
        try:
            re.compile(regex_pattern)
        except re.error:
            return JsonResponse({"error": "Expression régulière invalide"}, status=400)

        # Requête SQL pour rechercher dans title, authors et text_content
        sql_query = """
        SELECT *
        FROM books
        WHERE title ~* %s OR authors::TEXT ~* %s OR text_content ~* %s
        """
        results = execute_sql_query(sql_query, [regex_pattern, regex_pattern, regex_pattern])
        
        # Générer des suggestions basées sur les voisins
        suggestions = get_suggestions(results)

        page_result = results[offset:offset+limit]

        return JsonResponse({"results": page_result, "suggestions": suggestions}, status=200)
    except Exception as e:
        logger.error(f"Erreur lors de la recherche avancée avec regex='{regex_pattern}': {e}")
        return JsonResponse({"error": f"Erreur interne du serveur : {str(e)}"}, status=500)

def get_suggestions(top_results, max_suggestions=10):
    """
    Générer des suggestions basées sur les voisins des livres trouvés
    """
    try:
        if not top_results:
            return []
        
        # On regarde les voisins des 3 premiers résultats
        top_ids = [book['id'] for book in top_results[:3]]

        # Requête SQL pour récupérer les voisins
        sql_query = """
        SELECT *
        FROM books
        WHERE id IN (
            SELECT UNNEST(neighbors)
            FROM books
            WHERE id = ANY(%s)
        )
        ORDER BY centrality DESC
        LIMIT %s;
        """
        suggestions = execute_sql_query(sql_query, [top_ids, max_suggestions])

        return suggestions
    except Exception as e:
        logger.error(f"Erreur lors de la génération des suggestions: {e}")
        return []

# Implém algo

@cache_page(60 * 5)
@require_GET
def kmp_search_books(request):
    """
    Recherche KMP
    """
    try:
        pattern = request.GET.get('pattern', '').strip()
        if not pattern:
            return JsonResponse({"error": "Aucun pattern fourni."}, status=400)
        
        # s'il y a une limite en parametre
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))
        sort_by = request.GET.get('sort', '')

        
        books= []
        tokens = pattern.split()

        # pour chaque mot on fusionne les resultats de chaque requete pour un mot
        for token in tokens:
            pattern2 = f"%{token}%"
            sql_query = """
                SELECT id, title, authors, search_content, centrality, cover_url
                FROM books
                WHERE search_content @@ to_tsquery('simple', %s)
            """
            token_books = execute_sql_query(sql_query, [pattern2])
            books.extend(token_books)

        lps_map = {token: compute_lps(token) for token in tokens}
        full_lps = compute_lps(pattern)

        books = {book['id']: book for book in books}.values() # éliminer les doublons
        results = []
        for book in books:
            text = book.pop('search_content', '')
            title = book['title'] or ''
            authors = book['authors'] or ''
            
            occurrences_in_title = 0
            occurrences_in_text = 0
            occurences_in_authors= 0

            contains_full_pattern = (
                len(kmp_search_pos(title, pattern, full_lps)) > 0 or
                len(kmp_search_pos(text, pattern, full_lps)) > 0 or
                len(kmp_search_pos(authors, pattern, full_lps)) > 0
            )

            for pattern3, lps in lps_map.items():
                
                title_matches = kmp_search_pos(title, pattern3, lps)
                text_matches = kmp_search_pos(text, pattern3, lps)
                authors_matches = kmp_search_pos(authors, pattern3, lps)
                #logger.info(f"Title: {title}, Token: {pattern3}, Matches: {title_matches}")

                occurrences_in_title += len(title_matches)
                occurrences_in_text += len(text_matches)
                occurences_in_authors += len(authors_matches)

            # priorité pour le titre
            if occurrences_in_title > 0 or occurrences_in_text > 0 or occurences_in_authors > 0:
                book['occurrences_in_title'] = occurrences_in_title
                book['occurrences_in_text'] = occurrences_in_text
                book['occurrences_in_authors'] = occurences_in_authors
                book['contains_full_pattern'] = contains_full_pattern
                book['priority'] = 1 if occurrences_in_title > 0 else 2 if occurences_in_authors > 0 else 3
                book['total_occurrences'] = occurrences_in_title + occurrences_in_text + occurences_in_authors
                results.append(book)


        if sort_by == 'centrality':
            results.sort(key=lambda b: -b['centrality'])
        else:
            results.sort(
                key=lambda b: (
                    not b['contains_full_pattern'], # Priorité pour le pattern complet
                    b['priority'],                  # Priorité par titre > auteurs > texte
                    -b['occurrences_in_title'],     # Tri par occurrences dans le titre
                    -b['total_occurrences']         # Tri par nombre total d'occurrences
                )
            )

        page_result = results[offset:offset+limit]

        return JsonResponse({"results": page_result}, status=200)
    except Exception as e:
        logger.error(f"Erreur lors de la recherche KMP : {e}")
        return JsonResponse({"error": f"Erreur interne du serveur : {str(e)}"}, status=500)
    
import time
@cache_page(60 * 5)
@require_GET
def automate_regex_search_books(request):
    """
    Recherche RegEx via automate DFA
    """
    try:
        regex= request.GET.get('regex', '').strip()
        if not regex:
            return JsonResponse({"error": "Aucune expression régulière fournie."}, status=400)
        
        limit = int(request.GET.get('limit',10))
        offset = int(request.GET.get('offset', 0))
        sort_by = request.GET.get('sort', '')
        
        ttime = time.time()
        syntax_tree = parse(regex)
        nfa = to_ndfa(syntax_tree)
        dfa = ndfa_to_dfa(nfa)
        minimized_dfa = minimize_dfa(dfa)

        #regex = f"'{regex}'"
        sql_query = f"""
            SELECT id, title, authors, search_content, centrality, cover_url
            FROM books
        """
        books = execute_sql_query(sql_query, [regex])

        results = []
        for book in books:
            text = book.pop('search_content', '')
            title = book['title'] or ''
            authors = book['authors'] or ''
            
            occurrences_in_title = 0
            occurrences_in_text = 0
            occurences_in_authors= 0


            title_matches = search_regex(minimized_dfa, title)
            text_matches = search_regex(minimized_dfa, text)
            authors_matches = search_regex(minimized_dfa, authors)

            occurrences_in_title += len(title_matches)
            occurrences_in_text += len(text_matches)
            occurences_in_authors += len(authors_matches)

            # priorité pour le titre
            if occurrences_in_title > 0 or occurrences_in_text > 0 or occurences_in_authors > 0:
                book['occurrences_in_title'] = occurrences_in_title
                book['occurrences_in_text'] = occurrences_in_text
                book['occurences_in_authors'] = occurences_in_authors
                book['priority'] = 1 if occurrences_in_title > 0 else 2 if occurences_in_authors > 0 else 3
                book['total_occurrences'] = occurrences_in_title + occurrences_in_text + occurences_in_authors
                results.append(book)
                
        if sort_by == 'centrality':
            results.sort(key=lambda b: -b['centrality'])
        else:
            results.sort(key=lambda b: (b['priority'], -b['occurences_in_title'], -b['total_occurrences']))

        page_result = results[offset:offset+limit]
        endtime= time.time() - ttime

        print(f"Temps d'exécution : {endtime} secondes")
        return JsonResponse({"results": page_result}, status=200)

    except Exception as e:
        logger.error(f"Erreur lors de la recherche RegEx automate : {e}")
        return JsonResponse({"error": f"Erreur interne du serveur : {str(e)}"}, status=500)

@require_GET
def get_books_by_centrality(request):
    """
    Récupère la liste de tous les livres triés par centralité,
    avec limit/offset pour les pages
    """
    try:
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        sql_query = f"""
            SELECT id, title, authors, search_content, centrality, cover_url
            FROM books
            ORDER BY centrality DESC
            LIMIT %s
            OFFSET %s
        """
        books = execute_sql_query(sql_query, [limit, offset])

        for book in books:
            book.pop('search_content', None)

        return JsonResponse({"results": books}, status=200)
    except Exception as e:
        logger.error(f"Erreur lors de la récupération des livres : {e}")
        return JsonResponse({"error": f"Erreur interne du serveur : {str(e)}"}, status=500)