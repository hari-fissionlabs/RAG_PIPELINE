from psycopg2.extras import execute_values

class VectorStore:
    def __init__(self, conn, cur):
        self.conn = conn
        self.cur = cur
    
    def store_in_pgvector(self, chunks, embeddings):
        """Store chunks and embeddings in PostgreSQL PGVector"""
        if not chunks or not embeddings:
            return False
        
        try:
            data_to_insert = list(zip(chunks, embeddings))
            execute_values(
                self.cur,
                "INSERT INTO enhanced_documents (content, embedding) VALUES %s",
                data_to_insert
            )
            self.conn.commit()
            print(f"Successfully stored {self.cur.rowcount} documents in PGVector.")
            return True
        except Exception as e:
            print(f"Error storing in database: {e}")
            self.conn.rollback()
            return False