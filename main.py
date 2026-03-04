from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from supabase import create_client
import os, httpx
from bs4 import BeautifulSoup

app = FastAPI()

# جلب الإعدادات
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase = create_client(url, key)

@app.get("/fetch-news")
async def fetch_news():
    # المصادر المطلوبة حتماً
    sources = [
        {"n": "L'Usine Nouvelle", "u": "https://www.usinenouvelle.com/rss/"},
        {"n": "Les Echos", "u": "https://www.lesechos.fr/rss/rss_france.xml"}
    ]
    count = 0
    async with httpx.AsyncClient() as client:
        for s in sources:
            try:
                res = await client.get(s["u"], timeout=10.0)
                soup = BeautifulSoup(res.text, 'xml')
                for item in soup.find_all('item', limit=5):
                    # إدخال البيانات مع تجاوز الأخطاء
                    supabase.table("news").insert({
                        "title": item.title.text,
                        "link": item.link.text,
                        "media": s["n"]
                    }).execute()
                    count += 1
            except: continue
    return {"status": "success", "added": count}

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    try:
        # محاولة جلب البيانات
        res = supabase.table("news").select("*").order("created_at", desc=True).limit(10).execute()
        data = res.data
    except: data = []

    rows = "".join([f"<tr><td><b>{i['media']}</b></td><td>{i['title']}</td><td><a href='{i['link']}' target='_blank' style='color:#007bff;'>Lire</a></td></tr>" for i in data])

    return f"""
    <html>
        <head><title>IGH 2026</title><style>
            body {{ font-family: sans-serif; background: #f4f7f6; padding: 20px; }}
            .container {{ background: white; padding: 25px; border-radius: 12px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); max-width: 900px; margin: auto; }}
            h1 {{ color: #1a3a5a; border-left: 5px solid #007bff; padding-left: 15px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px; border-bottom: 1px solid #eee; text-align: left; }}
            th {{ background: #f8f9fa; }}
        </style></head>
        <body><div class="container">
            <h1>IGH 2026 : Intelligence Média & Innovation</h1>
            <p>Statut : <span style="color:green;">● Opérationnel</span> | Media : Les Echos, L'Usine Nouvelle</p>
            <table><thead><tr><th>Média</th><th>Titre de l'Actualité</th><th>Lien</th></tr></thead>
            <tbody>{rows if rows else "<tr><td colspan='3' style='text-align:center;'>Aucune donnée. Visitez /fetch-news pour charger.</td></tr>"}</tbody>
            </table>
        </div></body></html>
    """
