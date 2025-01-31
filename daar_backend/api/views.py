# daar_backend/api/views.py

from django.http import JsonResponse
from django.views.decorators.http import require_GET
import re
import logging
import json
from django.db import connection
from api.algorithms.kmp import compute_lps, kmp_search_pos
from api.algorithms.automate import search_regex, minimize_dfa, ndfa_to_dfa, to_ndfa, parse
from django.views.decorators.cache import cache_page
from collections import defaultdict

logger = logging.getLogger('api') 

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
        if not re.match(r'^\d+$', book_id):
            return JsonResponse({"error": "Format de book_id invalide"}, status=400)

        query = "SELECT * FROM books WHERE id = %s;"
        book = execute_sql_query(query, [book_id])
        
        if book:
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
        query = request.GET.get('q', '').strip()
        if not query:
            return JsonResponse({"error": "Aucun mot-clé fourni pour la recherche"}, status=400)
        
        if len(query) > 100:
            return JsonResponse({"error": "La requête est trop longue"}, status=400)

        # request body
        limit = int(request.GET.get('limit', 10)) # limite de livre 
        offset = int(request.GET.get('offset', 0)) # l'offset pour les pages
        sort_by = request.GET.get('sort', '') # criètre de tri

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
            results.sort(key=lambda b: (-b['rank'], -b['centrality']))
            
        else:
            results.sort(key=lambda b: -b['total_occurrences'])

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
        regex_pattern = request.GET.get('regex', '').strip()
        limit = int(request.GET.get('limit', 10))
        offset = int(request.GET.get('offset', 0))

        if not regex_pattern:
            return JsonResponse({"error": "Aucune expression régulière fournie"}, status=400)
        
        if len(regex_pattern) > 200:
            return JsonResponse({"error": "L'expression régulière est trop longue"}, status=400)
        
        try:
            re.compile(regex_pattern)
        except re.error:
            return JsonResponse({"error": "Expression régulière invalide"}, status=400)

        sql_query = """
        SELECT *
        FROM books
        WHERE title ~* %s OR authors::TEXT ~* %s OR text_content ~* %s
        """
        results = execute_sql_query(sql_query, [regex_pattern, regex_pattern, regex_pattern])
        
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

import time
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


def is_regex(pattern):
    special_chars = {'.', '*', '+', '?', '|', '[', ']', '(', ')', '{', '}', '\\', '^', '$'}
    return any(char in special_chars for char in pattern)


@cache_page(60 * 5)
@require_GET
def search(request):
    """
    Recherche par mot clé ou Regex
    Utilise KMP si mot clé ou automate DFA si Regex
    """
    pattern = request.GET.get('pattern', '').strip()
    if not pattern:
        return JsonResponse({"error": "Aucun pattern fourni."}, status=400)

    limit = int(request.GET.get('limit', 10))
    offset = int(request.GET.get('offset', 0))
    sort_by = request.GET.get('sort', '')

    book_scores = defaultdict(int)

    # requete dans la table d'indexage
    if is_regex(pattern):
        sql_indexage = "SELECT term, books_info FROM indexage"
        index_rows = execute_sql_query(sql_indexage)
    else:
        tokens = pattern.split()
        like_patterns = [f"{token}%" for token in tokens]
        sql_indexage = """
            SELECT term, books_info
              FROM indexage
             WHERE term ILIKE ANY(%s)
        """
        index_rows = execute_sql_query(sql_indexage, [like_patterns])

    # prétraitement
    if is_regex(pattern):
        syntax_tree = parse(pattern)
        nfa = to_ndfa(syntax_tree)
        dfa = ndfa_to_dfa(nfa)
        minimized_dfa = minimize_dfa(dfa)

        def term_matches(t):
            matches = search_regex(minimized_dfa, t.lower())
            return len(matches) > 0
    else:
        lps_map = {token: compute_lps(token) for token in tokens}

        def term_matches(t):
            t=t.lower()
            for token, lps in lps_map.items():
                if kmp_search_pos(t, token, lps):
                    return True
            return False

    # parcourir les résultats de l'indexage puis recherche dans la table des livres
    for row in index_rows:
        db_term = row["term"].lower()
        books_info = row["books_info"]
        if isinstance(books_info, str):
            books_info = json.loads(books_info)

        if term_matches(db_term):
            for item in books_info:
                b_id = item["book_id"]
                freq = item["freq"]
                book_scores[b_id] += freq

    if not book_scores:
        return JsonResponse({"results": []}, status=200)

    book_ids = list(book_scores.keys())
    sql_books = """
        SELECT id, title, authors, cover_url, centrality
          FROM books
         WHERE id = ANY(%s)
    """
    books_rows = execute_sql_query(sql_books, [book_ids])

    results = []
    for row in books_rows:
        b_id = row["id"]
        title = row["title"] or ""
        authors = row["authors"] or ""
        cover_url = row.get("cover_url")
        centrality = row.get("centrality", 0)
        total_occ = book_scores[b_id]

        priority = 3
        if is_regex(pattern):
            if search_regex(minimized_dfa, title):
                priority = 1
            elif search_regex(minimized_dfa, authors):
                priority = 2
        else:
            for token in tokens:
                lps = lps_map[token]
                if kmp_search_pos(title.lower(), token, lps):
                    priority = 1
                    break
                elif kmp_search_pos(authors.lower(), token, lps):
                    priority = 2

        results.append({
            "id": b_id,
            "title": title,
            "authors": authors,
            "cover_url": cover_url,
            "centrality": centrality,
            "total_occurrences": total_occ,
            "priority": priority
        })

    if sort_by == 'centrality':
        results.sort(key=lambda b: -b['centrality'] if b['centrality'] else 0)
    else:
        results.sort(
            key=lambda b: (
                b["priority"],
                -b["total_occurrences"]
            )
        )

    page_result = results[offset : offset + limit]
    return JsonResponse({"results": page_result}, status=200)
