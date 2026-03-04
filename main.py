from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from supabase import create_client
import os, httpx
from bs4 import BeautifulSoup

app = FastAPI()
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    # محاولة جلب الأخبار وتخزينها في جدول igh (الذي أصلحته أنت)
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

    # جلب البيانات من الجدول لعرضها
    res = supabase.table("igh").select("*").order("created_at", desc=True).limit(10).execute()
    data = res.data if res.data else []

    rows = "".join([f"<tr><td><b>{i['media']}</b></td><td>{i['title']}</td><td><a href='{i['link']}' target='_blank' style='color:#007bff;font-weight:bold;text-decoration:none;'>Consulter</a></td></tr>" for i in data])

    return f"""
    <html>
        <head><title>IGH 2026</title><style>
            body {{ font-family: sans-serif; background: #f8f9fa; padding: 20px; }}
            .card {{ background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); max-width: 900px; margin: auto; }}
            h1 {{ color: #1a3a5a; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 15px; border-bottom: 1px solid #eee; text-align: left; }}
        </style></head>
        <body><div class="card">
            <h1>IGH 2026 : Intelligence Média</h1>
            <p>Statut : <span style="color:green;font-weight:bold;">● Système Opérationnel</span></p>
            <table><thead><tr><th>Source</th><th>Titre</th><th>Lien</th></tr></thead>
            <tbody>{rows if rows else "<tr><td colspan='3' style='text-align:center; padding:40px;'>Initialisation... Veuillez rafraîchir la page (3 fois).</td></tr>"}</tbody>
            </table>
        </div></body></html>
    """
