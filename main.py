from fastapi import FastAPI
from supabase import create_client
import os

app = FastAPI(title="Backend IGH Zero-Cost")

# Connexion Supabase
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

@app.get("/")
def read_root():
    return {"Status": "Opérationnel", "Projet": "IGH 2026", "Architecture": "Zero-Cost"}

@app.get("/fetch-news")
def fetch_news():
    return {"message": "Moteur de collecte prêt"}

app = app
