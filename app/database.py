import psycopg
from dotenv import load_dotenv
import os
from psycopg.rows import dict_row

load_dotenv()

DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")

def connect_to_db():
    return psycopg.connect(dbname = 'gigkit',
                            user = 'postgres',
                            password = DATABASE_PASSWORD,
                            host = 'localhost',
                            port = 5432,
                            row_factory=dict_row
                            )

