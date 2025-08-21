from database_setup import DatabaseSetup
from text_processor import TextProcessor
from embedding_generator import EmbeddingGenerator
from vector_store import VectorStore
from retriever import Retriever
from generator import Generator

def main():
    """Main function that orchestrates all modules"""
    
    # Initialize all modules
    db_setup = DatabaseSetup()
    text_processor = TextProcessor()
    embedding_generator = EmbeddingGenerator()
    
    conn, cur = db_setup.get_connection()
    vector_store = VectorStore(conn, cur)
    retriever = Retriever(conn, cur)
    generator = Generator()
    
    try:
        # Step 1: Input and Extraction with chunk overlap
        print("=== Step 1: Input and Extraction ===")
        chunks = text_processor.input_and_extraction()
        
        if not chunks:
            print("No chunks extracted. Exiting.")
            return
        
        # Step 2: Generate Embeddings
        print("\n=== Step 2: Generate Embeddings ===")
        embeddings = embedding_generator.generate_embeddings(chunks)
        
        if not embeddings:
            print("No embeddings generated. Exiting.")
            return
        
        # Step 3: Store in PGVector
        print("\n=== Step 3: Store in PGVector ===")
        success = vector_store.store_in_pgvector(chunks, embeddings)
        
        if not success:
            print("Failed to store in database. Exiting.")
            return
        
        # Interactive Q&A Session
        print("\n" + "="*60)
        print("Interactive Q&A Session (type 'quit' to exit)")
        print("="*60)
        
        while True:
            user_query = input("\nEnter your question: ").strip()
            if user_query.lower() in ['quit', 'exit', 'q']:
                break
            
            if user_query:
                # Step 4: Retrieve chunks
                print("\n=== Step 4: Retrieval ===")
                retrieved_chunks = retriever.retrieve_chunks(user_query)
                
                # Step 5: Generate answer using retrieved chunks
                print("\n=== Step 5: Generation ===")
                answer = generator.generate_response(user_query, retrieved_chunks)
                print(f"\nFinal Generated Answer: {answer}")
                
    
    except KeyboardInterrupt:
        print("\nSession interrupted by user.")
    except Exception as e:
        print(f"Error in main execution: {e}")
    finally:
        # Clear database before closing
        print("\nCleaning up database...")
        try:
            cur.execute("DELETE FROM enhanced_documents;")
            conn.commit()
            print("Previous data cleared from database.")
        except Exception as e:
            print(f"Error clearing database: {e}")
        
        db_setup.close_connection()


if __name__ == "__main__":
    main()