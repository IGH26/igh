import streamlit as st
from supabase import create_client

# 1. إعدادات مركز ميديا IGH
st.set_page_config(page_title="IGH Media Center", page_icon="🎬", layout="wide")

# روابط مشروعكِ
URL = "https://rxxqnksutqrrhmdffpby.supabase.co"
KEY = "sb_publishable_am9iOnJ4eHFua3N1dHFycmhtZGZmcGJ5XzY0ZGNmMTItOGM2MC00YTQzLThmNzMtNjI5NTQyN2IxZjFi"

try:
    # الربط بقاعدة البيانات
    supabase = create_client(URL, KEY)
    
    # عنوان الموقع (تم تصحيح الخطأ هنا)
    st.markdown("<h1 style='text-align: center; color: #E91E63;'>🎬 مركز IGH الإعلامي 2026</h1>", unsafe_allow_html=True)
    st.divider()

    # جلب البيانات
    response = supabase.table('igh').select("*").execute()
    data = response.data

    if data:
        # عرض الأخبار في أعمدة احترافية
        cols = st.columns(2)
        for i, item in enumerate(data):
            with cols[i % 2]:
                with st.container(border=True):
                    # عرض الصورة إذا وجدت
                    img = item.get('image_url')
                    if img:
                        st.image(img, use_container_width=True)
                    
                    st.subheader(item.get('title', 'خبر جديد'))
                    
                    if item.get('link'):
                        st.link_button("📺 شاهد التغطية", item['link'])
    else:
        # رسالة تظهر إذا كان الجدول فارغاً
        st.info("📢 النظام متصل بنجاح! يرجى إضافة خبر في Supabase ليظهر هنا.")

except Exception as e:
    st.error(f"⚠️ حدث خطأ: {str(e)}")
