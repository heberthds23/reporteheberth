import os
import openai
openai.api_key = os.getenv('OPENAI_API_KEY')

def get_embedding(text: str):
    if not openai.api_key:
        # modo fallback: vector de ceros pequeño para poder probar
        return [0.0]*1536
    res = openai.Embedding.create(input=text, model='text-embedding-3-small')
    return res['data'][0]['embedding']
