from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from supabase import create_client
import os

app = FastAPI()

# إعدادات الربط الإلزامية
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    # جلب البيانات من الميديا المحددة (Les Echos, L'Usine Nouvelle...)
    try:
        response = supabase.table("news").select("*").order("created_at", desc=True).limit(10).execute()
        data = response.data
    except:
        data = []

    rows = "".join([f"<tr><td>{item['title']}</td><td><a href='{item['link']}' target='_blank'>Lien</a></td><td>{item.get('media', 'Direct')}</td></tr>" for item in data])

    return f"""
    <html>
        <head>
            <title>Dashboard IGH 2026</title>
            <style>
                body {{ font-family: sans-serif; background: #f4f7f6; padding: 30px; }}
                .container {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
                h1 {{ color: #1a3a5a; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
                th, td {{ padding: 12px; border: 1px solid #ddd; text-align: left; }}
                th {{ background: #007bff; color: white; }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>IGH 2026 : Intelligence Média & Innovation</h1>
                <p>Statut : <b>Opérationnel</b> | Media : <b>Les Echos, L'Usine Nouvelle</b></p>
                <table>
                    <thead><tr><th>Titre de l'Actualité</th><th>Source</th><th>Média</th></tr></thead>
                    <tbody>{rows if rows else "<tr><td colspan='3' style='text-align:center;'>Initialisation des flux média...</td></tr>"}</tbody>
                </table>
            </div>
        </body>
    </html>
    """

app = app
