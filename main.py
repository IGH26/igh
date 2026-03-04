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
    # Ici nous ajouterons plus tard le code de Scraping automatique
    # Pour l'instant, c'est le point d'entrée pour GitHub Actions
    return {"message": "Moteur de collecte prêt"}

# السطر الضروري لـ Vercel
app = app
