import streamlit as st
from supabase import create_client

# Configuration de la page
st.set_page_config(page_title="Dashboard IGH 2026", layout="wide", page_icon="📊")

# Connexion sécurisée
try:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    supabase = create_client(url, key)
except Exception:
    st.error("⚠️ Erreur : Clés API manquantes dans Streamlit Secrets.")

st.title("📊 Dashboard Média IGH 2026")
st.markdown("---")

# Onglets
tab1, tab2 = st.tabs(["🆕 Publier", "📰 Actualités"])

with tab1:
    with st.form("form_news", clear_on_submit=True):
        st.subheader("Nouvel Article")
        title = st.text_input("Titre de l'actualité")
        category = st.selectbox("Catégorie", ["Urgent", "Événement", "Sport", "Culture"])
        content = st.text_area("Texte de l'article")
        
        if st.form_submit_button("Publier sur le site"):
            if title and content:
                try:
                    supabase.table("news").insert({"title": title, "content": content, "category": category}).execute()
                    st.success("✅ Publié avec succès !")
                except Exception as e:
                    st.error(f"Erreur : {e}")
            else:
                st.warning("Veuillez remplir tous les champs.")

with tab2:
    st.subheader("Articles récents")
    try:
        res = supabase.table("news").select("*").order("created_at", desc=True).execute()
        for item in res.data:
            with st.expander(f"📌 {item['title']} ({item['category']})"):
                st.write(item['content'])
                if st.button("Supprimer", key=item['id']):
                    supabase.table("news").delete().eq("id", item['id']).execute()
                    st.rerun()
    except Exception:
        st.info("Aucune donnée disponible pour le moment.")
