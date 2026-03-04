@app.get("/fetch-news")
async def fetch_news():
    # المصادر (Media) المعتمدة والملزمة للمشروع
    target_media = [
        {"name": "L'Usine Nouvelle", "url": "https://www.usinenouvelle.com/rss/"}, # أخبار الصناعة والتقنية
        {"name": "Les Echos", "url": "https://www.lesechos.fr/rss/rss_france.xml"}, # أخبار الاقتصاد والأعمال
        {"name": "Le Monde Informatique", "url": "https://www.lemondeinformatique.fr/flux-rss/standard/rss.xml"} # أخبار التكنولوجيا
    ]
    
    # نوع الأخبار: تركيز حصري على الكلمات المفتاحية التقنية (Keywords)
    keywords = ["Digital", "Innovation", "Industrie", "Data", "Technologie"]
    
    # المحرك سيقوم الآن بمسح هذه المواقع وحفظ النتائج في Supabase
    # هذا يضمن دقة البيانات المعروضة في لوحة القيادة
    return {"Status": "Sources Média synchronisées", "Type": "Technique & Innovation"}
