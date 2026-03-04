import streamlit as st
import pandas as pd
from supabase import create_client

# 1. إعدادات واجهة الموقع
st.set_page_config(page_title="منصة IGH للأخبار", page_icon="📰", layout="wide")

# 2. روابط الربط (تم تصحيحها بدقة من صورك 1000064331 و 1000064332)
URL = "https://rxxqnksutqrrhmdffpby.supabase.co"
KEY = "sb_publishable_am9iOnJ4eHFua3N1dHFycmhtZGZmcGJ5XzY0ZGNmMTItOGM2MC00YTQzLThmNzMtNjI5NTQyN2IxZjFi"

# 3. محاولة الاتصال وعرض البيانات
try:
    supabase = create_client(URL, KEY)
    
    st.markdown("<h1 style='text-align: center; color: #1E88E5;'>📱 منصة الأخبار الذكية - IGH</h1>", unsafe_content_type=True)
    st.write("---")

    # جلب البيانات من جدول igh
    response = supabase.table('igh').select("*").execute()
    data = response.data

    if data and len(data) > 0:
        for item in data:
            with st.container():
                st.subheader(f"📌 {item.get('title', 'خبر جديد')}")
                st.write(item.get('content', 'لا يوجد محتوى حالياً.'))
                if item.get('link'):
                    st.link_button("🔗 قراءة الخبر كاملاً", item['link'])
                st.divider()
    else:
        st.balloons()
        st.success("✅ مبروك! الموقع يعمل ومرتبط بنجاح بـ Supabase.")
        st.info("الموقع فارغ حالياً. جربي إضافة خبر من لوحة تحكم Supabase!")

except Exception as e:
    st.error(f"⚠️ خطأ في الاتصال: تأكدي من إعدادات الـ API في Supabase.")
