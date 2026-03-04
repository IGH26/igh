import streamlit as st
from supabase import create_client

# 1. إعدادات مركز ميديا IGH
st.set_page_config(page_title="IGH Media Center", page_icon="🎬", layout="wide")

# روابط مشروعكِ (تأكدي من نسخها كاملة كما هي هنا)
URL = "https://rxxqnksutqrrhmdffpby.supabase.co"
KEY = "sb_publishable_am9iOnJ4eHFua3N1dHFycmhtZGZmcGJ5XzY0ZGNmMTItOGM2MC00YTQzLThmNzMtNjI5NTQyN2IxZjFi"

try:
    # الربط بقاعدة البيانات
    supabase = create_client(URL, KEY)
    
    # عنوان الموقع
    st.markdown("<h1 style='text-align: center; color: #E91E63;'>🎬 مركز IGH 2026 الإعلامي</h1>", unsafe_allow_html=True)
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
                    # عرض الصورة من عمود image_url الذي أنشأتِه
                    img = item.get('image_url')
                    if img:
                        st.image(img, use_container_width=True)
                    
                    st.subheader(item.get('title', 'خبر جديد'))
                    
                    if item.get('link'):
                        st.link_button("📺 شاهد التغطية", item['link'])
    else:
        # هذه الرسالة ستظهر لأن جدولكِ فارغ حالياً
        st.balloons()
        st.info("✅ النظام متصل! اذهبي لـ Supabase وأضيفي أول سطر (Insert Row) لترى الميديا هنا.")

except Exception as e:
    st.error("⚠️ تأكدي من تحديث ملف app.py بالكود الجديد ومسح الكود القديم تماماً.")
