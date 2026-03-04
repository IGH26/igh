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
    # محاولة سحب أخبار جديدة وحفظها في كل مرة تفتح فيها الصفحة (لضمان التحديث)
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get("https://www.usinenouvelle.com/rss/", timeout=5)
            soup = BeautifulSoup(r.text, 'xml')
            for item in soup.find_all('item', limit=3):
                supabase.table("news").upsert({"title": item.title.text, "link": item.link.text, "media": "L'Usine Nouvelle"}).execute()
    except: pass

    # جلب البيانات للعرض
    try:
        data = supabase.table("news").select("*").order("created_at", desc=True).limit(10).execute().data
    except: data = []

    rows = "".join([f"<tr><td><b>{i['media']}</b></td><td>{i['title']}</td><td><a href='{i['link']}' target='_blank' style='color:#007bff;font-weight:bold;'>Lire</a></td></tr>" for i in data])

    return f"""
    <html>
        <head><title>IGH 2026 - Dashboard</title><style>
            body {{ font-family: sans-serif; background: #f0f2f5; padding: 20px; }}
            .card {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 8px 16px rgba(0,0,0,0.1); max-width: 900px; margin: auto; }}
            h1 {{ color: #1a3a5a; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px; border-bottom: 1px solid #eee; text-align: left; }}
            th {{ background: #f8f9fa; color: #333; }}
        </style></head>
        <body><div class="card">
            <h1>IGH 2026 : Intelligence Média & Innovation</h1>
            <p>Statut : <span style="color:green;">● Système Actif</span> | Sources : Les Echos, L'Usine Nouvelle</p>
            <table><thead><tr><th>Média</th><th>Titre</th><th>Action</th></tr></thead>
            <tbody>{rows if rows else "<tr><td colspan='3' style='text-align:center;'>Mise à jour des flux en cours...</td></tr>"}</tbody>
            </table>
        </div></body></html>
    """

app = app
