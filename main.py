from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from supabase import create_client
import os, httpx
from bs4 import BeautifulSoup

app = FastAPI()
supabase = create_client(os.environ.get("SUPABASE_URL"), os.environ.get("SUPABASE_KEY"))

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    # محاولة جلب الأخبار وحفظها
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get("https://www.usinenouvelle.com/rss/", timeout=5)
            soup = BeautifulSoup(r.text, 'xml')
            for item in soup.find_all('item', limit=3):
                supabase.table("igh").upsert({
                    "title": item.title.text,
                    "link": item.link.text,
                    "media": "L'Usine Nouvelle"
                }).execute()
    except:
        pass

    # جلب البيانات للعرض
    data = supabase.table("igh").select("*").order("created_at", desc=True).execute().data or []
    
    # تحويل البيانات إلى صفوف في الجدول
    rows = "".join([f"<tr><td>{i['media']}</td><td>{i['title']}</td><td><a href='{i['link']}' target='_blank'>Lire</a></td></tr>" for i in data])

    return f"""
    <html>
        <head><style>
            body {{ font-family: sans-serif; padding: 40px; background: #f4f7f6; }}
            .box {{ background: white; padding: 20px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px; border: 1px solid #ddd; text-align: left; }}
            th {{ background: #007bff; color: white; }}
        </style></head>
        <body>
            <div class="box">
                <h1>IGH 2026 - Dashboard PRO</h1>
                <table>
                    <thead><tr><th>Média</th><th>Titre</th><th>Lien</th></tr></thead>
                    <tbody>{rows if rows else "<tr><td colspan='3' style='text-align:center;'>Aucune donnée. Vérifiez le SQL Editor et rafraîchissez.</td></tr>"}</tbody>
                </table>
            </div>
        </body>
    </html>
    """
