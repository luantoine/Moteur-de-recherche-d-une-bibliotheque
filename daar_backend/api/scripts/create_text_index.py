import os
import psycopg2
import json
import re
from collections import Counter, defaultdict
from dotenv import load_dotenv
from psycopg2.extras import execute_batch

load_dotenv()

conn = psycopg2.connect(
    dbname=os.getenv('DB_NAME', 'defaultdb'),
    port=os.getenv('DB_PORT', '5432'),
    user=os.getenv('DB_USER', 'avnadmin'),
    password=os.getenv('DB_PASSWORD', ''),
    host=os.getenv('DB_HOST', 'localhost')
)

cursor = conn.cursor()

def load_words():
    words = set()
    for lang in ['fr', 'en']:
        try:
            with open(f"filtre/{lang}_filtre.txt", "r", encoding="utf-8") as f:
                words.update(line.strip().lower() for line in f if line.strip())
        except FileNotFoundError:
            print(f"Fichier filtre/{lang}_filtre.txt manquant")
    return words

def clean_text(text, stopwords):
    text = re.sub(r"[^\w\s-]", " ", text)
    tokens = text.split()

    filtered = []
    for w in tokens:
        wl = w.lower()
        if wl in stopwords:
            continue
        if wl.isdigit():
            continue
        if re.match(r"^-+$", wl):
            continue

        filtered.append(w)

    return filtered

def create_table():
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS indexage (
            term TEXT PRIMARY KEY,
            books_info JSONB NOT NULL DEFAULT '[]'
        );
    """)
    conn.commit()

def extract_authors(authors):
    if not authors:
        return ""
    if isinstance(authors, list):
        return " ".join(a["name"] if isinstance(a, dict) and "name" in a else str(a) for a in authors)
    try:
        parsed = json.loads(authors)
        return " ".join(a["name"] if isinstance(a, dict) and "name" in a else str(a) for a in parsed)
    except json.JSONDecodeError:
        return ""



def load_indexage(terms):
    existing = {}
    CHUNK_SIZE = 5000
    terms_list = list(terms)
    for i in range(0, len(terms_list), CHUNK_SIZE):
        subset = terms_list[i:i+CHUNK_SIZE]
        cursor.execute("SELECT term, books_info FROM indexage WHERE term = ANY(%s);", (subset,))
        for row in cursor:
            existing[row[0]] = row[1]
    return existing

def merge_termFreq(global_terms, existing):
    for term, books_info in existing.items():
        if term not in global_terms:
            global_terms[term] = Counter()
        for book in books_info:
            global_terms[term][book["book_id"]] += book["freq"]

def update_indexage(global_terms):
    data = [(term, json.dumps([{"book_id": bid, "freq": f} for bid, f in books.items()])) for term, books in global_terms.items()]
    query = """
        INSERT INTO indexage(term, books_info) VALUES (%s, %s)
        ON CONFLICT (term) DO UPDATE SET books_info = EXCLUDED.books_info;
    """
    CHUNK_SIZE = 5000
    for i in range(0, len(data), CHUNK_SIZE):
        execute_batch(cursor, query, data[i:i+CHUNK_SIZE])
        conn.commit()

def build_index(chunk_size=200):
    cursor.execute("SELECT COUNT(*) FROM books;")
    total_books = cursor.fetchone()[0]
    print(f"Total livres {total_books}")
    offset = 0
    stopwords = load_words()
    while True:
        print(f"Traitement chunk {chunk_size} livres à partir de {offset}")
        cursor.execute("SELECT id, title, authors, text_content FROM books ORDER BY id LIMIT %s OFFSET %s;", (chunk_size, offset))
        rows = cursor.fetchall()
        if not rows:
            break
        global_terms = defaultdict(Counter)
        for book_id, title, authors, text in rows:
            text = f"{title or ''} {extract_authors(authors)} {text[:200000] or ''}"
            tokens = clean_text(text, stopwords)
            cursor.execute("UPDATE books SET search_content = to_tsvector('simple', %s) WHERE id = %s;", (" ".join(tokens), book_id))
            for term, freq in Counter(tokens).items():
                global_terms[term.lower()][book_id] += freq
        existing = load_indexage(global_terms.keys())
        merge_termFreq(global_terms, existing)
        update_indexage(global_terms)
        conn.commit()
        offset += len(rows)
    print("Indexation terminée")

def main():
    try:
        create_table()
        cursor.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1 FROM information_schema.columns WHERE table_name = 'books' AND column_name = 'search_content'
                ) THEN ALTER TABLE books ADD COLUMN search_content tsvector;
            END $$;
        """)
        conn.commit()
        build_index()
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_books_search ON books USING gin(search_content);")
        conn.commit()
        print("Indexation terminée")
    except Exception as e:
        conn.rollback()
        print(f"Erreur {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
