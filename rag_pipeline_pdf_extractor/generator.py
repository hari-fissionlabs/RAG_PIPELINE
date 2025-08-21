from flotorch_core.inferencer.gateway_inferencer import GatewayInferencer
from dotenv import load_dotenv
from prompts import prompts
import os

load_dotenv()

class Generator:
    def __init__(self):
        pass
    
    def generate_response(self, question, retrieved_chunks):
        """Generate response using LLM with joined chunks as single context string"""
        if not retrieved_chunks:
            return "I don't know."
        
        try:
            # Join all retrieved chunks into a single string
            joined_context = " ".join(retrieved_chunks)
            context = [{'text': joined_context}]
            
            # System prompt guide object
            n_shot_prompt_guide = {
                "system_prompt": (
                    "You are a helpful assistant that answers questions based strictly on the provided context. "
                    "Provide clear, accurate answers in 2-3 sentences. "
                    "If the context doesn't contain relevant information, respond with 'I don't know.' "
                    "Do not use external knowledge beyond the given context."
                )
            }
            
            print(f"Generating response for: {question}")
            print(f"Joined {len(retrieved_chunks)} chunks into single context string")

            
            # Initialize GatewayInferencer with only required parameters
            inferencer = GatewayInferencer(
                model_id="bedrock/us.amazon.nova-lite-v1:0",
                api_key=os.getenv("API_KEY"),
                base_url=os.getenv("BASE_URL"),
                n_shot_prompt_guide_obj=n_shot_prompt_guide,
                n_shot_prompts=2
            )
            
            # Generate text with joined context string
            metadata, answer = inferencer.generate_text(question, context)
            
            # Check if response is HTML (API error)
            if answer and answer.strip().startswith('<!DOCTYPE'):
                print("Received HTML response - API endpoint issue")
                return self._fallback_response(question, joined_context)
            
            if not answer or len(answer.strip()) < 10:
                return "I don't know."
            
            # Return clean answer
            clean_answer = answer.strip()
            # print(f"Generated answer: {clean_answer[:100]}...")
            return clean_answer
            
        except Exception as e:
            print(f"Generation error: {str(e)}")
            return self._fallback_response(question, " ".join(retrieved_chunks))
    
    def _fallback_response(self, question, context):
        """Provide fallback response when LLM fails"""
        # Simple keyword matching fallback
        question_lower = question.lower()
        context_lower = context.lower()
        
        if "machine learning" in question_lower and "machine learning" in context_lower:
            # Find sentence containing machine learning
            sentences = context.split('.')
            for sentence in sentences:
                if "machine learning" in sentence.lower():
                    return sentence.strip() + "."
        
        # Generic fallback
        return f"Based on the available context: {context[:300]}..."