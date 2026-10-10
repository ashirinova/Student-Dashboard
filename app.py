import streamlit as st
import pandas as pd
import plotly.express as px
from database import init_db, add_student, get_students, get_student, update_student_score, delete_student
from services import calculate_grade, calculate_statistics, get_grade_distribution
from config import GRADE_COLORS

# Səhifə konfiqurasiyası
st.set_page_config(
    page_title="Pro Student Analytics Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Bazanı başlanğıcda hazırlayırıq
init_db()

# Xüsusi Vizual Stil
st.markdown("""
    <style>
    .main { padding: 1rem; }
    .stMetric { background-color: #f8f9fa; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
""", unsafe_allow_html=True)

st.title("🎓 UniversityDB - Student Analytics Dashboard")

# Bütün məlumatları gətiririk
raw_students = get_students()
stats = calculate_statistics(raw_students)

# Üst KPI Paneli
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Students", stats["total_students"])
col2.metric("Average Score", f"{stats['average_score']} / 100")
col3.metric("Highest Score", f"🔥 {stats['highest_score']}")
col4.metric("Lowest Score", f"⚠️ {stats['lowest_score']}")
col5.metric("Pass Rate", f"✅ {stats['pass_rate']}%")

st.divider()

# Tab-lar
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Dashboard & Qrafiklər", 
    "📋 Tələbə Siyahısı & İxrac", 
    "➕ Yeni Tələbə Əlavə Et", 
    "⚙️ İdarəetmə Paneli (Edit/Delete)"
])

# Tab 1: Qrafiklər və Vizual Təhlil
with tab1:
    st.subheader("Vizual Analitika")
    if raw_students:
        chart_col1, chart_col2 = st.columns(2)
        
        grade_dist = get_grade_distribution(raw_students)
        df_dist = pd.DataFrame(list(grade_dist.items()), columns=['Grade', 'Count'])
        
        with chart_col1:
            st.markdown("**Grade-lərin Paylanması (Pie Chart)**")
            fig_pie = px.pie(
                df_dist, values='Count', names='Grade', 
                color='Grade', color_discrete_map=GRADE_COLORS,
                hole=0.4
            )
            st.plotly_chart(fig_pie, use_container_width=True)
            
        with chart_col2:
            st.markdown("**Qiymət Histoqramı (Bar Chart)**")
            df_students = pd.DataFrame([
                {"Name": s[1], "Score": s[2], "Grade": calculate_grade(s[2])} 
                for s in raw_students
            ])
            fig_bar = px.bar(
                df_students, x='Name', y='Score', color='Grade',
                color_discrete_map=GRADE_COLORS, text='Score'
            )
            st.plotly_chart(fig_bar, use_container_width=True)
    else:
        st.info("Qrafiklərin görünməsi üçün baza boş olmamalıdır.")

# Tab 2: Siyahı və İxrac (CSV/Excel)
with tab2:
    st.subheader("Tələbələrin Tam Siyahısı")
    
    # Filtrləmə və Axtarış
    search_term = st.text_input("🔍 Tələbə adına görə sürətli axtarış:")
    filtered_data = get_student(search_term) if search_term else raw_students

    if filtered_data:
        data_list = [
            {
                "ID": student[0],
                "Name": student[1],
                "Score": student[2],
                "Grade": calculate_grade(student[2])
            }
            for student in filtered_data
        ]
        df_display = pd.DataFrame(data_list)
        st.dataframe(df_display, use_container_width=True)
        
        # CSV olaraq İxrac etmək düyməsi (Vau Effekti)
        csv = df_display.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Siyahını CSV Kimi Yüklə",
            data=csv,
            file_name='students_performance.csv',
            mime='text/csv'
        )
    else:
        st.warning("Məlumat tapılmadı.")

# Tab 3: Yeni Tələbə Əlavə Etmək
with tab3:
    st.subheader("Baza Üçün Yeni Tələbə Qeydiyyatı")
    with st.form("add_student_form", clear_on_submit=True):
        student_name = st.text_input("Tələbənin Adı və Soyadı")
        student_score = st.number_input("Topladığı Bal (0 - 100)", min_value=0.0, max_value=100.0, step=1.0)
        submit_button = st.form_submit_button("➕ Tələbəni Əlavə Et")

        if submit_button:
            if student_name.strip():
                if add_student(student_name.strip(), student_score):
                    st.success(f"🎉 '{student_name}' uğurla bazaya əlavə olundu!")
                    st.balloons() # Şənlik effekti!
                    st.rerun()
                else:
                    st.error("Xəta baş verdi.")
            else:
                st.warning("Lütfən ad xanasını doldurun.")

# Tab 4: Silmək və Düzəliş etmək (Full CRUD)
with tab4:
    st.subheader("⚙️ Məlumatların İdarə Edilməsi")
    if raw_students:
        student_dict = {f"{s[1]} (ID: {s[0]}, Bal: {s[2]})": s for s in raw_students}
        selected_option = st.selectbox("Tələbəni seçin:", list(student_dict.keys()))
        selected_student = student_dict[selected_option]

        col_edit, col_del = st.columns(2)
        
        with col_edit:
            st.markdown("### ✏️ Balı Yenilə")
            new_score = st.number_input("Yeni bal daxil edin:", min_value=0.0, max_value=100.0, value=float(selected_student[2]))
            if st.button("Balı Yenilə"):
                if update_student_score(selected_student[0], new_score):
                    st.success("Bal yeniləndi!")
                    st.rerun()

        with col_del:
            st.markdown("### 🗑️ Tələbəni Sil")
            if st.button("Tələbəni Bazadan Sil", type="primary"):
                if delete_student(selected_student[0]):
                    st.warning("Tələbə silindi!")
                    st.rerun()