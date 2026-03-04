from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from supabase import create_client
import os, httpx
from bs4 import BeautifulSoup

app = FastAPI()

# الاتصال بـ Supabase
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    # محاولة جلب الأخبار تلقائياً عند فتح الصفحة لملء الجدول
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get("https://www.usinenouvelle.com/rss/", timeout=10)
            soup = BeautifulSoup(r.text, 'xml')
            for item in soup.find_all('item', limit=5):
                supabase.table("news").upsert({
                    "title": item.title.text,
                    "link": item.link.text,
                    "media": "L'Usine Nouvelle"
                }).execute()
    except: pass

    # جلب البيانات للعرض
    try:
        data = supabase.table("news").select("*").order("created_at", desc=True).limit(10).execute().data
    except: data = []

    rows = "".join([f"<tr><td><b>{i['media']}</b></td><td>{i['title']}</td><td><a href='{i['link']}' target='_blank' style='color:#007bff;font-weight:bold;text-decoration:none;'>Lire l'article</a></td></tr>" for i in data])

    return f"""
    <html>
        <head>
            <title>IGH 2026 - Dashboard</title>
            <style>
                body {{ font-family: 'Segoe UI', sans-serif; background: #f0f2f5; padding: 20px; }}
                .card {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); max-width: 1000px; margin: auto; }}
                h1 {{ color: #1a3a5a; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
                table {{ width: 100%; border-collapse: collapse; margin-top: 25px; }}
                th, td {{ padding: 15px; border-bottom: 1px solid #eee; text-align: left; }}
                th {{ background: #f8f9fa; color: #333; }}
                .status {{ color: #28a745; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="card">
                <h1>IGH 2026 : Intelligence Média & Innovation</h1>
                <p>Statut : <span class="status">● Système Opérationnel</span> | Media : Les Echos, L'Usine Nouvelle</p>
                <table>
                    <thead><tr><th>Média Source</th><th>Titre de l'Actualité</th><th>Action</th></tr></thead>
                    <tbody>{rows if rows else "<tr><td colspan='3' style='text-align:center; padding:30px;'>Initialisation... Veuillez rafraîchir la page.</td></tr>"}</tbody>
                </table>
            </div>
        </body>
    </html>
    """
