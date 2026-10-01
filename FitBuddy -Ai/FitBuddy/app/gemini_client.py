from functools import lru_cache
from .config import GOOGLE_API_KEY,GEMINI_MODEL
@lru_cache
def get_client():
    if not GOOGLE_API_KEY: return None
    from google import genai
    return genai.Client(api_key=GOOGLE_API_KEY)
def generate(prompt:str)->str:
    c=get_client()
    if c is None: return ""
    r=c.models.generate_content(model=GEMINI_MODEL,contents=prompt)
    return (r.text or "").strip()
