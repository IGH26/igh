import streamlit as st
from supabase import create_client

# إعدادات الصفحة الاحترافية
st.set_page_config(page_title="لوحة تحكم IGH 2026", layout="wide", page_icon="📊")

# جلب البيانات من Secrets
url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
supabase = create_client(url, key)

# التصميم العلوي (Header)
st.title("📊 لوحة تحكم مركز IGH 2026 الإعلامي")
st.markdown("---")

# إنشاء تبويبات (Tabs) لتنظيم العمل
tab1, tab2, tab3 = st.tabs(["🆕 إضافة خبر جديد", "📝 إدارة الأخبار", "📈 الإحصائيات"])

# --- التبويب الأول: إضافة خبر ---
with tab1:
    col1, col2 = st.columns([2, 1])
    with col1:
        with st.form("main_form", clear_on_submit=True):
            st.subheader("تفاصيل الخبر")
            title = st.text_input("عنوان الخبر الرئيسي")
            category = st.selectbox("التصنيف", ["عاجل", "فعاليات", "تغطية خاصة", "بيان صحفي"])
            content = st.text_area("نص الخبر الكامل", height=200)
            
            uploaded_file = st.file_uploader("إرفاق صورة الخبر", type=['jpg', 'png', 'jpeg'])
            
            submit = st.form_submit_button("نشر الآن على الموقع")
            
            if submit:
                if title and content:
                    # عملية الإدخال في Supabase
                    data = {"title": title, "content": content, "category": category}
                    supabase.table("news").insert(data).execute()
                    st.success(f"✅ تم نشر الخبر بنجاح في قسم {category}")
                else:
                    st.error("الرجاء إكمال جميع الحقول")
    
    with col2:
        st.info("💡 **نصيحة:** استخدم عناوين قصيرة وجذابة لزيادة التفاعل مع الأخبار.")
        st.image("https://images.unsplash.com/photo-1495020689067-958852a7765e?w=400", caption="معاينة التنسيق")

# --- التبويب الثاني: إدارة الأخبار ---
with tab2:
    st.subheader("الأخبار المنشورة")
    # جلب البيانات من Supabase لعرضها
    response = supabase.table("news").select("*").order("created_at", desc=True).execute()
    news_list = response.data
    
    if news_list:
        for item in news_list:
            with st.expander(f"📌 {item['title']} - ({item['category']})"):
                st.write(item['content'])
                st.caption(f"تاريخ النشر: {item.get('created_at', 'غير محدد')}")
    else:
        st.write("لا توجد أخبار منشورة حالياً.")

# --- التبويب الثالث: الإحصائيات ---
with tab3:
    st.subheader("أداء المركز الإعلامي")
    c1, c2, c3 = st.columns(3)
    c1.metric("إجمالي الأخبار", len(news_list) if news_list else 0)
    c2.metric("الصور المرفوعة", "12", "+2 اليوم")
    c3.metric("المشاهدات", "1,240", "15%+")
