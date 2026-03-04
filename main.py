from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from supabase import create_client
import os
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

# إعدادات الربط
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

# 1. وظيفة جلب الأخبار (يجب أن تكون في الأعلى)
@app.get("/fetch-news")
async def fetch_news():
    sources = [
        {"name": "L'Usine Nouvelle", "url": "https://www.usinenouvelle.com/rss/"},
        {"name": "Les Echos", "url": "https://www.lesechos.fr/rss/rss_france.xml"}
    ]
    added = 0
    async with httpx.AsyncClient() as client:
        for src in sources:
            try:
                r = await client.get(src["url"])
                soup = BeautifulSoup(r.text, 'xml')
                for item in soup.find_all('item', limit=3):
                    supabase.table("news").insert({
                        "title": item.title.text,
                        "link": item.link.text,
                        "media": src["name"]
                    }).execute()
                    added += 1
            except: continue
    return {"Status": "Succès", "Articles": added}

# 2. واجهة العرض الرئيسية
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    try:
        data = supabase.table("news").select("*").order("created_at", desc=True).limit(10).execute().data
    except: data = []
    
    rows = "".join([f"<tr><td><b>{i['media']}</b></td><td>{i['title']}</td><td><a href='{i['link']}' target='_blank'>Lire</a></td></tr>" for i in data])

    return f"""
    <html>
        <head><title>IGH 2026</title><style>
            body {{ font-family: sans-serif; background: #f8f9fa; padding: 20px; }}
            .card {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px; border-bottom: 1px solid #eee; text-align: left; }}
            th {{ background: #1a3a5a; color: white; }}
        </style></head>
        <body><div class="card">
            <h2>IGH 2026 : Intelligence Média</h2>
            <table><thead><tr><th>Média</th><th>Titre</th><th>Action</th></tr></thead>
            <tbody>{rows if rows else "<tr><td colspan='3'>Cliquez sur /fetch-news pour charger les données.</td></tr>"}</tbody>
            </table>
        </div></body></html>
    """
