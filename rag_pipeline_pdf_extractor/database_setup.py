import psycopg2

class DatabaseSetup:
    def __init__(self):
        self.db_connect_string = "dbname=postgres user=postgres password=3485 host=localhost port=5433"
        self.conn = None
        self.cur = None
        self.setup_database()
    
    def setup_database(self):
        """Setup database connection and table"""
        try:
            self.conn = psycopg2.connect(self.db_connect_string)
            self.cur = self.conn.cursor()
            print("Database connection successful.")
            
            self.cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
            self.cur.execute("""
                CREATE TABLE IF NOT EXISTS enhanced_documents (
                    id SERIAL PRIMARY KEY,
                    content TEXT,
                    embedding VECTOR(768)
                );
            """)
            self.conn.commit()
            print("'enhanced_documents' table is ready.")
        except Exception as e:
            print(f"Database setup error: {e}")
            exit()
    
    def get_connection(self):
        return self.conn, self.cur
    
    def close_connection(self):
        """Close database connection"""
        if self.cur:
            self.cur.close()
        if self.conn:
            self.conn.close()
        print("Database connection closed.")