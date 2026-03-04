import streamlit as st
from supabase import create_client

# إعدادات مركز الميديا
st.set_page_config(page_title="IGH Media Center", page_icon="🎬", layout="wide")

URL = "https://rxxqnksutqrrhmdffpby.supabase.co"
KEY = "sb_publishable_am9iOnJ4eHFua3N1dHFycmhtZGZmcGJ5XzY0ZGNmMTItOGM2MC00YTQzLThmNzMtNjI5NTQyN2IxZjFi"

try:
    supabase = create_client(URL, KEY)
    st.markdown("<h1 style='text-align: center; color: #E91E63;'>🎬 مركز IGH الإعلامي 2026</h1>", unsafe_content_type=True)
    st.write("---")

    # جلب البيانات
    response = supabase.table('igh').select("*").order('created_at', desc=True).execute()
    data = response.data

    if data:
        # عرض الأخبار في شبكة احترافية
        cols = st.columns(2)
        for i, item in enumerate(data):
            with cols[i % 2]:
                with st.container(border=True):
                    img = item.get('image_url')
                    if img:
                        st.image(img, use_container_width=True)
                    st.subheader(item.get('title'))
                    if item.get('link'):
                        st.link_button("📺 شاهد التغطية", item['link'])
    else:
        st.info("📢 ننتظر رفع المواد الإعلامية لجدول igh...")

except Exception as e:
    st.error("⚠️ تأكدي من إعدادات قاعدة البيانات وإضافة عمود image_url")
