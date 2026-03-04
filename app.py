import streamlit as st
from supabase import create_client

# إعدادات الواجهة
st.set_page_config(page_title="لوحة تحكم IGH 2026", layout="wide")

# الربط (تأكد أن الأسماء مطابقة لـ Secrets)
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

st.title("📊 لوحة تحكم مركز IGH 2026")

# تجربة جلب البيانات مع معالجة الخطأ
try:
    res = supabase.table("news").select("*").execute()
    st.success("✅ النظام متصل وجاهز!")
    
    # واجهة إضافة الأخبار
    with st.form("add_news"):
        title = st.text_input("عنوان الخبر")
        content = st.text_area("نص الخبر")
        if st.form_submit_button("نشر"):
            supabase.table("news").insert({"title": title, "content": content}).execute()
            st.rerun()

except Exception as e:
    st.error(f"يوجد مشكلة في الجدول: {e}")
    st.info("إذا رأيت هذا الخطأ، اضغط على Reboot App من قائمة Manage app")
