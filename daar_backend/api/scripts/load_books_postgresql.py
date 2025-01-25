import os
import sys
import requests
import psycopg2
from psycopg2.extras import Json
from time import sleep
from tqdm import tqdm


# Connexion à PostgreSQL
conn = psycopg2.connect(
    dbname="library_db",
    port="5432",
    user="postgres",
    password="daar2025",
    host="db"
)
cursor = conn.cursor()

def fetch_and_store_books(limit=1664):
    """
    Récupère jusqu'à limit livres depuis l'API Gutendex :
      - L'id
      - Le titre
      - La liste d'auteurs, de sujets, de langues, etc.
      - Le lien vers le texte brut (text_url) s'il existe
      - Le lien vers l'image de couverture (cover_url) s'il existe
      - Les autres informations qui pourront être utiles
    """
    base_url = "https://gutendex.com/books/"
    page_url = base_url
    fetched_count = 0

    while page_url and fetched_count < limit:
        print(f"[*] Récupération de la page : {page_url}")
        resp = requests.get(page_url)
        if resp.status_code != 200:
            print(f"    > Impossible de charger la page {page_url}, arrêt")
            continue

        data = resp.json()
        results = data.get("results", [])
        next_url = data.get("next")

        for book in tqdm(results):
            if fetched_count >= limit:
                break

            book_id = str(book["id"])
            title = book["title"]
            authors = book.get("authors", [])
            subjects = book.get("subjects", [])
            bookshelves = book.get("bookshelves", [])
            languages = book.get("languages", [])
            copyright_ = book.get("copyright", False)
            media_type = book.get("media_type", "Text")
            download_count = book.get("download_count", 0)
            formats = book.get("formats", {})

            # URL texte
            text_url = None
            for fkey, fval in formats.items():
                if fkey.startswith("text/plain"):
                    text_url = fval
                    break

            # URL image 
            cover_url = formats.get("image/jpeg", None)

            # Télécharger le texte pour avoir tout le texte du livre
            text_content = None
            if text_url:
                try:
                    text_resp = requests.get(text_url)
                    if text_resp.status_code == 200:
                        text_content = text_resp.text.replace('\x00', '')
                    else:
                        print(f"    > Impossible de télécharger le texte pour {title} (ID={book_id})")
                except Exception as e:
                    print(f"    > Erreur lors du téléchargement du texte pour {title} : {e}")

            # vers PostgreSQL (DB Name = library_db)
            try:
                cursor.execute("""
                    INSERT INTO books (
                        book_id, title, authors, subjects, bookshelves,
                        languages, copyright, media_type, download_count,
                        text_content, cover_url
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (book_id) DO UPDATE SET
                        title = EXCLUDED.title,
                        authors = EXCLUDED.authors,
                        subjects = EXCLUDED.subjects,
                        bookshelves = EXCLUDED.bookshelves,
                        languages = EXCLUDED.languages,
                        copyright = EXCLUDED.copyright,
                        media_type = EXCLUDED.media_type,
                        download_count = EXCLUDED.download_count,
                        text_content = EXCLUDED.text_content,
                        cover_url = EXCLUDED.cover_url;
                """, (
                    book_id, title, Json(authors), Json(subjects), Json(bookshelves),
                    Json(languages), copyright_, media_type, download_count,
                    text_content, cover_url
                ))
                conn.commit()
                fetched_count += 1
                print(f"    > Livre '{title}' (ID={book_id}) inséré/mis à jour. (Total={fetched_count})")
            except psycopg2.Error as e:
                print(f"[ERREUR] Échec de l'insertion/mise à jour du livre ID={book_id} : {e}")
                conn.rollback()

            sleep(0.01)

        page_url = next_url

    print(f"=== Fin {fetched_count} livres stockés ou mis à jour ===")

def main():
    fetch_and_store_books(limit=1664)

if __name__ == "__main__":
    main()
