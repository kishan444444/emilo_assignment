from project.logger import logging
from project.exception import customexception
import sys
import os
from dotenv import load_dotenv


# Load variables from .env into the system's environment
load_dotenv()

api_key = os.getenv("API_KEY")

from groq import Groq

client = Groq(api_key=api_key)

def understand_query_llm(user_query):
    try:
        prompt = f"""
        
        You are an AI assistant for an e-commerce recommendation system.

        Your task is to understand the user's intent and convert it into a clear, standardized shopping occasion query.

        Rules:
        - Focus on intent, not exact words
        - Normalize into common shopping occasions
        - Keep output short (2–4 words)
        - Always return a product-focused query 
        - Do NOT explain anything
        - Do NOT return multiple options
        
        


        Query: {user_query}
        Return ONLY the normalized query.
        """

        response = client.chat.completions.create(
            model= "llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=20
        )

        return response.choices[0].message.content.strip().lower()

    except:
        return user_query.lower()



def generate_reason_llm(product, query):
    
    try:
        prompt = f"""
        User query: {query}
        Product: {product['name']}
        Description: {product.get('shortDescription','')}

        Explain in ONE short sentence why this product is relevant.
        """

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",   
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=40
        )

        return response.choices[0].message.content.strip()
    
    except Exception as e:
                logging.info("Exception occured in load_object file utils")
                raise customexception(e,sys)
    

    
