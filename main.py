from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from supabase import create_client
import os, httpx
from bs4 import BeautifulSoup

app = FastAPI()
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    # محاولة سحب الأخبار
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get("https://www.usinenouvelle.com/rss/", timeout=10)
            soup = BeautifulSoup(r.text, 'xml')
            for item in soup.find_all('item', limit=5):
                supabase.table("igh").upsert({
                    "title": item.title.text,
                    "link": item.link.text,
                    "media": "L'Usine Nouvelle"
                }).execute()
    except: pass

    # عرض البيانات
    data = supabase.table("igh").select("*").order("created_at", desc=True).execute().data or []
    rows = "".join([f"<tr><td><b>{i['media']}</b></td><td>{i['title']}</td><td><a href='{i['link']}' target='_blank'>VOIR</a></td></tr>" for i in data])

    return f"""
    <html>
        <head><style>
            body {{ font-family: sans-serif; padding: 20px; background: #f0f2f5; }}
            .card {{ background: white; padding: 25px; border-radius: 10px; max-width: 800px; margin: auto; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
            h1 {{ color: #1a3a5a; border-left: 5px solid #007bff; padding-left: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px; border-bottom: 1px solid #eee; text-align: left; }}
        </style></head>
        <body><div class="card">
            <h1>IGH 2026 : Système Opérationnel</h1>
            <table><thead><tr><th>Source</th><th>Actualité</th><th>Lien</th></tr></thead>
            <tbody>{rows if rows else "<tr><td colspan='3' style='text-align:center;'>Connexion établie. Rafraîchissez la page une fois.</td></tr>"}</tbody>
            </table>
        </div></body></html>
    """
