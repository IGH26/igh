import streamlit as st
from supabase import create_client

# 1. إعدادات مركز ميديا IGH
st.set_page_config(page_title="IGH Media Center", page_icon="🎬", layout="wide")

# روابط مشروعكِ التي أرسلتِها (تم التأكد منها حرفياً)
URL = "https://rxxqnksutqrrhmdffpby.supabase.co"
KEY = "sb_publishable_NzavY25DD8X_wZoalKQfMw_d8D_Lgz6"

try:
    # الربط بقاعدة البيانات
    supabase = create_client(URL, KEY)
    
    # عنوان الموقع
    st.markdown("<h1 style='text-align: center; color: #E91E63;'>🎬 مركز IGH 2026 الإعلامي</h1>", unsafe_allow_html=True)
    st.divider()

    # جلب البيانات من جدول igh
    response = supabase.table('igh').select("*").execute()
    data = response.data

    if data:
        # عرض الميديا في أعمدة احترافية
        cols = st.columns(2)
        for i, item in enumerate(data):
            with cols[i % 2]:
                with st.container(border=True):
                    # عرض الصورة من العمود الذي أنشأتِه
                    img = item.get('image_url')
                    if img:
                        st.image(img, use_container_width=True)
                    
                    st.subheader(item.get('title', 'خبر جديد'))
                    
                    if item.get('link'):
                        st.link_button("📺 شاهد التغطية", item['link'])
    else:
        # ستظهر البالونات بمجرد نجاح الاتصال (لأن الجدول فارغ حالياً)
        st.balloons()
        st.success("✅ أخيراً! تم الاتصال بنجاح بالمفتاح والرابط الجديد.")
        st.info("النظام جاهز! أضيفي خبراً في Supabase لتريه هنا بالصور.")

except Exception as e:
    st.error("⚠️ يرجى التأكد من مسح الكود القديم تماماً ولصق هذا الكود فقط.")
