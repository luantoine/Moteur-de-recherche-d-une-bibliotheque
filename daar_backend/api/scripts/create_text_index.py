import psycopg2
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, "../../.."))
sys.path.append(project_root) 
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daar_backend.daar_backend.settings')
from daar_backend.settings import DATABASES


def create_text_index():
    try:
        db_config = DATABASES['default']
        # Connexion à PostgreSQL
        conn = psycopg2.connect(
            dbname=db_config['NAME'],
            user=db_config['USER'],
            password=db_config['PASSWORD'],
            host=db_config['HOST'],
            port=db_config['PORT']
        )
        cursor = conn.cursor()

        # colonne `search_content`
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

        cursor.execute("""
            UPDATE books
            SET search_content = to_tsvector(
                'english',
                title || ' ' || (
                    SELECT string_agg(value, ' ')
                    FROM jsonb_array_elements_text(authors) AS value
                )
            );
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_books_search
            ON books USING gin(search_content);
        """)

        conn.commit()
        print("Index textuel créé avec succès.")

    except Exception as e:
        print(f"Erreur lors de la création de l'index textuel : {e}")

    finally:
        if conn:
            cursor.close()
            conn.close()


if __name__ == "__main__":
    create_text_index()
