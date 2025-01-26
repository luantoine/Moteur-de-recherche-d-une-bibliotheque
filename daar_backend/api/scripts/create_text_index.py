import psycopg2
import os
import sys
import json
import re

conn = psycopg2.connect(
    dbname="defaultdb",
    port="25492",
    user="avnadmin",
    password="AVNS_swNH8lITHgvFjg-tf5M",
    host="daar2025-luluantoinex-745c.b.aivencloud.com"
)
cursor = conn.cursor()

def load_stopwords():
    stopwords = set()
    try:
        with open("filtre/fr_filtre.txt", "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip().lower()
                if word:
                    stopwords.add(word)
    except FileNotFoundError:
        print("Le fichier 'filtre/fr_filtre.txt' est introuvable, aucun stopword FR n'a été chargé.")

    try:
        with open("filtre/en_filtre.txt", "r", encoding="utf-8") as f:
            for line in f:
                word = line.strip().lower()
                if word:
                    stopwords.add(word)
    except FileNotFoundError:
        print("Le fichier 'filtre/en_filtre.txt' est introuvable, aucun stopword EN n'a été chargé.")

    return stopwords

def create_text_index():
    try:
        stopwords = load_stopwords()

        # Vérifier et ajouter la colonne `search_content` si elle n'existe pas
        cursor.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (
                    SELECT 1
                    FROM information_schema.columns
                    WHERE table_name = 'books' AND column_name = 'search_content'
                ) THEN
                    ALTER TABLE books ADD COLUMN search_content tsvector;
                END IF;
            END $$;
        """)

        # Récupérer la table `books`
        cursor.execute("""
            SELECT id, title, authors, text_content
            FROM books
        """)
        rows = cursor.fetchall()

        for row in rows:
            book_id = row[0]
            title = row[1] or ""
            authors_data = row[2]  # Peut être None, liste, ou string JSON
            text_content = row[3] or ""

            # -- Gérer authors_data --
            if not authors_data:
                authors_list = []
            elif isinstance(authors_data, list):
                # Déjà une liste Python => on la traite
                authors_list = []
                for a in authors_data:
                    if isinstance(a, dict):
                        # On récupère le champ 'name' s'il existe,
                        # sinon on convertit tout en string
                        if "name" in a:
                            authors_list.append(a["name"])
                        else:
                            authors_list.append(str(a))
                    else:
                        # Si c'est déjà une str ou autre
                        authors_list.append(str(a))
            else:
                # Sinon, c'est probablement une chaîne JSON => on parse
                try:
                    parsed = json.loads(authors_data)
                    if isinstance(parsed, list):
                        authors_list = []
                        for a in parsed:
                            if isinstance(a, dict):
                                if "name" in a:
                                    authors_list.append(a["name"])
                                else:
                                    authors_list.append(str(a))
                            else:
                                authors_list.append(str(a))
                    else:
                        # Si ce n'est pas une liste, on ignore
                        authors_list = []
                except json.JSONDecodeError:
                    authors_list = []

            truncated_text = text_content[:200000]

            # Concaténer : on utilise la liste authors_list de chaînes
            combined_text = f"{title} " + " ".join(authors_list) + " " + truncated_text

            # Nettoyer la ponctuation => remplace [^\w\s-] par espace
            combined_text = re.sub(r"[^\w\s-]", " ", combined_text)

            # Split
            words = combined_text.split()

            # Filtrer les stopwords
            filtered_words = [w for w in words if w.lower() not in stopwords]

            # Rejoindre
            final_text = " ".join(filtered_words)

            # Mettre à jour la colonne
            cursor.execute("""
                UPDATE books
                SET search_content = to_tsvector('simple', %s)
                WHERE id = %s
            """, (final_text, book_id))

        # Créer index GIN
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_books_search
            ON books USING gin(search_content);
        """)

        conn.commit()
        print("Index textuel créé et mis à jour avec succès.")

    except Exception as e:
        print(f"Erreur lors de la création ou de la mise à jour de l'index textuel : {e}")
        conn.rollback()
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    create_text_index()
