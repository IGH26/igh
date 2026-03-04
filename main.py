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
    # محاولة سحب أخبار حقيقية وحفظها في جدول igh
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get("https://www.usinenouvelle.com/rss/", timeout=10)
            soup = BeautifulSoup(r.text, 'xml')
            items = soup.find_all('item', limit=5)
            
            for item in items:
                # محاولة إدخال البيانات في جدول igh
                supabase.table("igh").upsert({
                    "title": item.title.text,
                    "link": item.link.text,
                    "media": "L'Usine Nouvelle"
                }).execute()
    except Exception as e:
        print(f"Erreur: {e}")

    # جلب البيانات من جدول igh للعرض
    try:
        res = supabase.table("igh").select("*").order("created_at", desc=True).limit(10).execute()
        data = res.data if res.data else []
    except:
        data = []

    rows = "".join([f"<tr><td><b>{i['media']}</b></td><td>{i['title']}</td><td><a href='{i['link']}' target='_blank' style='color:#007bff;font-weight:bold;text-decoration:none;'>Consulter</a></td></tr>" for i in data])

    return f"""
    <html>
        <head><title>IGH Dashboard 2026</title><style>
            body {{ font-family: sans-serif; background: #f8f9fa; padding: 20px; }}
            .container {{ background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); max-width: 950px; margin: auto; }}
            h1 {{ color: #1a3a5a; border-left: 6px solid #007bff; padding-left: 15px; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 25px; }}
            th, td {{ padding: 15px; border-bottom: 1px solid #eee; text-align: left; }}
            th {{ background: #f1f3f5; font-size: 12px; text-transform: uppercase; }}
            .status {{ background: #d4edda; color: #155724; padding: 5px 12px; border-radius: 20px; font-size: 13px; font-weight: bold; }}
        </style></head>
        <body><div class="container">
            <h1>IGH 2026 : Intelligence & Innovation</h1>
            <p><span class="status">SYSTÈME ACTIF</span> | Base de données : <b>Table IGH</b></p>
            <table><thead><tr><th>Média</th><th>Titre de l'Actualité</th><th>Action</th></tr></thead>
            <tbody>{rows if rows else "<tr><td colspan='3' style='text-align:center; padding:40px;'>Initialisation des données... Veuillez rafraîchir la page dans 10 secondes.</td></tr>"}</tbody>
            </table>
        </div></body></html>
    """
