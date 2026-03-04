import streamlit as st
from supabase import create_client

# إعداد واجهة احترافية
st.set_page_config(page_title="IGH 2026 Dashboard", layout="wide")

# جلب بيانات الربط من Secrets
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("📊 لوحة تحكم مركز IGH 2026")

# تقسيم الشاشة لتبويبات
tab1, tab2 = st.tabs(["📝 إضافة خبر", "📰 عرض الأخبار"])

with tab1:
    with st.form("news_form", clear_on_submit=True):
        title = st.text_input("عنوان الخبر")
        category = st.selectbox("التصنيف", ["عاجل", "فعاليات", "تقارير"])
        content = st.text_area("نص الخبر")
        submit = st.form_submit_button("نشر الآن")
        
        if submit and title and content:
            supabase.table("news").insert({"title": title, "content": content, "category": category}).execute()
            st.success("✅ تم النشر بنجاح!")

with tab2:
    # جلب الأخبار من الجدول الذي أنشأته في SQL
    res = supabase.table("news").select("*").order("created_at", desc=True).execute()
    for item in res.data:
        with st.expander(f"📌 {item['title']} ({item['category']})"):
            st.write(item['content'])
