import google.generativeai as genai

class Retriever:
    def __init__(self, conn, cur):
        self.api_key = "AIzaSyAfSTIaHE2ac7zWA5-VjRPHjlSOZplbLc4"
        genai.configure(api_key=self.api_key)
        self.embedding_model = "models/embedding-001"
        self.conn = conn
        self.cur = cur
    
    def retrieve_chunks(self, question):
        """Retrieve relevant chunks from database"""
        try:
            query_embedding_response = genai.embed_content(
                model=self.embedding_model,
                content=question,
                task_type="RETRIEVAL_QUERY"
            )
            query_embedding = query_embedding_response['embedding']
            
            self.cur.execute(
                "SELECT content, embedding <=> %s as distance FROM enhanced_documents ORDER BY embedding <=> %s LIMIT 3",
                (str(query_embedding), str(query_embedding))
            )
            results = self.cur.fetchall()
            
            if not results:
                return []
            
            # Check if most relevant chunk is similar enough (distance < 1.2)
            if results[0][1] > 1.2:
                return []
            
            # Return list of chunks
            chunks = [row[0] for row in results]
            
            # Display retrieved chunks for user
            # print("Retrieved relevant chunks:")
            for i, chunk in enumerate(chunks, 1):
                print(f"\nChunk {i}: {chunk}")
            
            return chunks
                
        except Exception as e:
            print(f"Error retrieving chunks: {e}")
            return []