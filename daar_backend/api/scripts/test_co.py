#!/usr/bin/env python3
import psycopg2
import sys

conn = psycopg2.connect(
    dbname="defaultdb",
    port="25492",
    user="avnadmin",
    password="AVNS_swNH8lITHgvFjg-tf5M",
    host="daar2025-luluantoinex-745c.b.aivencloud.com"
)
cursor = conn.cursor()

def main():
    try:
        conn.autocommit = True
        cursor = conn.cursor()

        # 1) Enable the pg_trgm extension
        cursor.execute("CREATE EXTENSION IF NOT EXISTS pg_trgm;")
        print("Extension pg_trgm créée (ou déjà existante).")


        # 3) Create a trigram index on text_content
        #    This speeds up ILIKE '%pattern%' queries.
        create_index_sql = """
        CREATE INDEX IF NOT EXISTS trigram
            ON books
            USING GIN (text_content gin_trgm_ops);
        """
        cursor.execute(create_index_sql)
        print("Index trigram sur text_content créé (ou déjà existant).")


        cursor.close()
        conn.close()
        print("Configuration terminée.")
    except Exception as e:
        print(f"Erreur lors de la configuration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
