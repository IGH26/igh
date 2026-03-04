import streamlit as st
from supabase import create_client

# 1. إعدادات مركز ميديا IGH
st.set_page_config(page_title="IGH Media Center", page_icon="🎬", layout="wide")

# الروابط الصحيحة والمراجعة بدقة من صورك
URL = "https://rxxqnksutqrrhmdffpby.supabase.co"
KEY = "sb_publishable_am9iOnJ4eHFua3N1dHFycmhtZGZmcGJ5XzY0ZGNmMTItOGM2MC00YTQzLThmNzMtNjI5NTQyN2IxZjFi"

try:
    # الاتصال بقاعدة البيانات
    supabase = create_client(URL, KEY)
    
    # عنوان الموقع
    st.markdown("<h1 style='text-align: center; color: #E91E63;'>🎬 مركز IGH 2026 الإعلامي</h1>", unsafe_allow_html=True)
    st.divider()

    # جلب البيانات من جدول igh
    response = supabase.table('igh').select("*").execute()
    data = response.data

    if data:
        # عرض الأخبار في أعمدة احترافية (الميديا التي طلبها المدير)
        cols = st.columns(2)
        for i, item in enumerate(data):
            with cols[i % 2]:
                with st.container(border=True):
                    # عرض الصورة من عمود image_url
                    img = item.get('image_url')
                    if img:
                        st.image(img, use_container_width=True)
                    
                    st.subheader(item.get('title', 'خبر جديد'))
                    
                    if item.get('link'):
                        st.link_button("📺 شاهد التغطية", item['link'])
    else:
        # رسالة النجاح والبالونات (ستظهر لأن الجدول فارغ حالياً)
        st.balloons()
        st.success("✅ تم الربط بنجاح مذهل!")
        st.info("النظام متصل! اذهبي لـ Supabase وأضيفي خبر في جدول igh ليظهر هنا بالصور.")

except Exception as e:
    st.error("⚠️ تأكدي من مسح الكود القديم ولصق هذا الكود الجديد بالكامل.")
