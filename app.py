import streamlit as st
from supabase import create_client

# إعدادات مركز ميديا IGH
st.set_page_config(page_title="IGH Media Center", page_icon="🎬", layout="wide")

# روابط مشروعكِ الحقيقية
URL = "https://rxxqnksutqrrhmdffpby.supabase.co"
KEY = "sb_publishable_am9iOnJ4eHFua3N1dHFycmhtZGZmcGJ5XzY0ZGNmMTItOGM2MC00YTQzLThmNzMtNjI5NTQyN2IxZjFi"

try:
    supabase = create_client(URL, KEY)
    st.markdown("<h1 style='text-align: center; color: #E91E63;'>🎬 مركز IGH الإعلامي 2026</h1>", unsafe_content_type=True)
    st.write("---")

    # جلب البيانات من الجدول
    response = supabase.table('igh').select("*").order('created_at', desc=True).execute()
    data = response.data

    if data:
        # عرض البيانات في شبكة (Columns)
        cols = st.columns(2)
        for i, item in enumerate(data):
            with cols[i % 2]:
                with st.container(border=True):
                    # عرض الصورة
                    img = item.get('image_url')
                    if img:
                        st.image(img, use_container_width=True)
                    else:
                        st.image("https://via.placeholder.com/800x400?text=IGH+News", use_container_width=True)
                    
                    st.subheader(item.get('title', 'خبر جديد'))
                    st.caption(f"📅 التاريخ: {item.get('created_at', 'غير متوفر')}")
                    
                    if item.get('link'):
                        st.link_button("📺 شاهد التغطية الكاملة", item['link'])
    else:
        st.balloons()
        st.info("📢 النظام جاهز! أضيفي أول خبر مع رابط صورة في Supabase لتبدأ الميديا بالظهور.")

except Exception as e:
    st.error(f"⚠️ تنبيه: {str(e)}")
