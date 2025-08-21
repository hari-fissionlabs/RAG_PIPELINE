from pypdf import PdfReader

class TextProcessor:
    def __init__(self):
        self.chunk_size = 1024
        self.overlap_percentage = 20
    
    def input_and_extraction(self):
        """Input taking and text extraction with chunk overlap"""
        file_path = input("Enter file path (.pdf or .txt): ").strip()
        
        chunks = []
        if file_path.endswith('.pdf'):
            print(f"\nProcessing PDF: {file_path}")
            reader = PdfReader(file_path)
            full_text = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    full_text += page_text + " "
        elif file_path.endswith('.txt'):
            print(f"\nProcessing text file: {file_path}")
            with open(file_path, 'r', encoding='utf-8') as f:
                full_text = f.read()
        else:
            print("Unsupported file format")
            return []
        
        # Create overlapping chunks
        overlap_size = int(self.chunk_size * self.overlap_percentage / 100)
        start = 0
        
        while start < len(full_text):
            end = start + self.chunk_size
            chunk = full_text[start:end].strip()
            
            if len(chunk) > 50:  # Only add substantial chunks
                chunks.append(chunk)
            
            # Move start position with overlap
            start = end - overlap_size
            
            if end >= len(full_text):
                break
        
        print(f"Created {len(chunks)} overlapping chunks (chunk size: {self.chunk_size}, overlap: {self.overlap_percentage}%)")
        return chunks