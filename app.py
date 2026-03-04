import streamlit as st
import pandas as pd
from supabase import create_client

# إعداد واجهة الموقع
st.set_page_config(page_title="تطبيق الأخبار IGH", layout="wide")
st.title("📰 منصة الأخبار الذكية - IGH")

# بيانات الربط مع Supabase (سنملأها في الخطوة القادمة)
URL = "رابط_مشروعك_هنا"
KEY = "مفتاح_API_الخاص_بك_هنا"

try:
    supabase = create_client(URL, KEY)
    
    # جلب البيانات من جدول igh
    response = supabase.table('igh').select("*").execute()
    data = response.data

    if data:
        df = pd.DataFrame(data)
        for index, row in df.iterrows():
            with st.container():
                st.subheader(row['title'])
                st.write(f"🔗 [رابط الخبر]({row['link']})")
                st.caption(f"📅 تاريخ النشر: {row['date']}")
                st.divider()
    else:
        st.warning("المخزن فارغ حالياً! نحن بانتظار وصول الأخبار الجديدة.")

except Exception as e:
    st.error(f"خطأ في الاتصال بالقاعدة: {e}")
