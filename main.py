from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from supabase import create_client
import os, httpx
from bs4 import BeautifulSoup

app = FastAPI()

# الربط بـ Supabase
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    # سحب أخبار جديدة وحفظها في جدول igh
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get("https://www.usinenouvelle.com/rss/", timeout=10)
            soup = BeautifulSoup(r.text, 'xml')
            for item in soup.find_all('item', limit=5):
                # التوجيه لجدول igh حصراً
                supabase.table("igh").upsert({
                    "title": item.title.text,
                    "link": item.link.text,
                    "media": "L'Usine Nouvelle"
                }).execute()
    except: pass

    # جلب البيانات من جدول igh للعرض
    try:
        data = supabase.table("igh").select("*").order("created_at", desc=True).limit(10).execute().data
    except: data = []

    rows = "".join([f"<tr><td><b>{i['media']}</b></td><td>{i['title']}</td><td><a href='{i['link']}' target='_blank' style='color:#007bff;font-weight:bold;text-decoration:none;'>Consulter</a></td></tr>" for i in data])

    return f"""
    <html>
        <head><title>IGH Dashboard 2026</title><style>
            body {{ font-family: 'Segoe UI', sans-serif; background: #f8f9fa; padding: 20px; }}
            .container {{ background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); max-width: 950px; margin: auto; }}
            h1 {{ color: #1a3a5a; border-left: 6px solid #007bff; padding-left: 15px; margin-bottom: 5px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 25px; }}
            th, td {{ padding: 15px; border-bottom: 1px solid #eee; text-align: left; }}
            th {{ background: #f1f3f5; color: #495057; font-size: 12px; text-transform: uppercase; }}
            .status-tag {{ background: #d4edda; color: #155724; padding: 5px 12px; border-radius: 20px; font-size: 13px; font-weight: bold; }}
        </style></head>
        <body><div class="container">
            <h1>IGH 2026 : Intelligence & Innovation</h1>
            <p><span class="status-tag">SYSTÈME ACTIF</span> | Base de données : <b>Table IGH</b></p>
            <table><thead><tr><th>Média</th><th>Titre de l'Actualité</th><th>Action</th></tr></thead>
            <tbody>{rows if rows else "<tr><td colspan='3' style='text-align:center; padding:40px;'>Synchronisation avec la table IGH... Actualisez la page.</td></tr>"}</tbody>
            </table>
        </div></body></html>
    """
