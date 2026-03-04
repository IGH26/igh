from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from supabase import create_client
import os

app = FastAPI()

# الاتصال بـ Supabase
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

@app.get("/", response_class=HTMLResponse)
def dashboard():
    return """
    <html>
        <head>
            <title>IGH Dashboard 2026</title>
            <style>
                body { font-family: sans-serif; background: #f4f7f6; padding: 40px; }
                .container { max-width: 800px; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
                h1 { color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px; }
                .status { background: #d4edda; color: #155724; padding: 10px; border-radius: 5px; margin: 20px 0; }
                .card { border-left: 5px solid #3498db; padding: 10px; background: #f9f9f9; margin-top: 20px; }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Tableau de Bord - IGH 2026</h1>
                <div class="status">● Système Opérationnel (Hébergé sur Vercel)</div>
                <div class="card">
                    <h3>Statistiques du Projet</h3>
                    <p><b>Architecture:</b> Zero-Cost (Gratuit)</p>
                    <p><b>Base de données:</b> Connectée (Supabase)</p>
                </div>
                <p style="margin-top:20px; color: #7f8c8d;">Prêt pour la collecte automatique des actualités.</p>
            </div>
        </body>
    </html>
    """

app = app
