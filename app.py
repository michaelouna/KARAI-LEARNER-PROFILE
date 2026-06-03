import streamlit as st
import pandas as pd
import os

# Configuration and File Paths
CSV_FILE = 'KARAI SCHOOL REGISTRY - STUDENTS.csv'

# Column names from your registry schema
COLUMNS = [
    'Admission_No', 'First_Name', 'Middle_Name', 'Surname', 'UPI_Number', 
    'DOB', 'Gender', 'Birth_Cert_No', 'Grade_Level', 'Stream', 
    'Special_Needs', 'Parent_National_ID', 'Birth_Cert_Image', 'Status'
]

def load_data():
    if os.path.exists(CSV_FILE):
        try:
            df = pd.read_csv(CSV_FILE)
            if df.empty and len(df.columns) == 0:
                df = pd.DataFrame(columns=COLUMNS)
            return df
        except Exception as e:
            return pd.DataFrame(columns=COLUMNS)
    else:
        df = pd.DataFrame(columns=COLUMNS)
        df.to_csv(CSV_FILE, index=False)
        return df

def save_data(df):
    # Ensure columns order matches perfectly
    df = df[COLUMNS]
    df.to_csv(CSV_FILE, index=False)

# Initialize app data
df = load_data()

# Ensure proper schema compliance
for col in COLUMNS:
    if col not in df.columns:
        df[col] = None

# Ensure proper data types for key lookup columns
df['Admission_No'] = df['Admission_No'].astype(str)

st.set_page_config(page_title="Karai School Registry App", page_icon="🏫", layout="wide")
st.title("🏫 Karai School Registry - Students' Profile App")

# Sidebar navigation
st.sidebar.title("📌 Menu Navigation")
page = st.sidebar.radio("Go to:", ["📊 Dashboard Overview", "🔍 Search & Profiles", "➕ Add New Student", "✏️ Edit Student Profile"])

# Help button to load sample demo data if empty
if df.empty or len(df) == 0:
    st.sidebar.info("💡 The registry database is currently empty.")
    if st.sidebar.button("✨ Populate with Sample Data"):
        sample_data = [
            {'Admission_No': '101', 'First_Name': 'John', 'Middle_Name': 'K.', 'Surname': 'Maina', 'UPI_Number': 'UPI987654A', 'DOB': '2012-04-12', 'Gender': 'Male', 'Birth_Cert_No': 'BC12345', 'Grade_Level': 'Grade 6', 'Stream': 'Red', 'Special_Needs': 'None', 'Parent_National_ID': '12345678', 'Birth_Cert_Image': '', 'Status': 'Active'},
            {'Admission_No': '102', 'First_Name': 'Grace', 'Middle_Name': 'W.', 'Surname': 'Njoroge', 'UPI_Number': 'UPI123456B', 'DOB': '2011-09-23', 'Gender': 'Female', 'Birth_Cert_No': 'BC67890', 'Grade_Level': 'Grade 7', 'Stream': 'Blue', 'Special_Needs': 'Asthma', 'Parent_National_ID': '87654321', 'Birth_Cert_Image': '', 'Status': 'Active'},
            {'Admission_No': '103', 'First_Name': 'Brian', 'Middle_Name': 'O.', 'Surname': 'Omondi', 'UPI_Number': 'UPI555666C', 'DOB': '2010-01-15', 'Gender': 'Male', 'Birth_Cert_No': 'BC11223', 'Grade_Level': 'Grade 8', 'Stream': 'Red', 'Special_Needs': 'None', 'Parent_National_ID': '23456789', 'Birth_Cert_Image': '', 'Status': 'Active'}
        ]
        df = pd.DataFrame(sample_data)
        save_data(df)
        st.success("Sample data generated!")
        st.rerun()

# --- PAGES ---

if page == "📊 Dashboard Overview":
    st.header("📊 Registry Overview Dashboard")
    if df.empty:
        st.info("No data available. Please click 'Populate with Sample Data' or go to 'Add New Student' to begin.")
    else:
        # KPI metrics
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Registered Students", len(df))
        c2.metric("Active Student Base", len(df[df['Status'] == 'Active']))
        c3.metric("Boys / Male Count", len(df[df['Gender'] == 'Male']))
        c4.metric("Girls / Female Count", len(df[df['Gender'] == 'Female']))
        
        st.subheader("📋 Complete Student Roster")
        st.dataframe(df[['Admission_No', 'First_Name', 'Surname', 'Grade_Level', 'Stream', 'Status']], use_container_width=True)
        
        st.subheader("📈 School Distribution Insights")
        col_chart1, col_chart2 = st.columns(2)
        with col_chart1:
            st.markdown("**Students by Grade Level**")
            grade_counts = df['Grade_Level'].value_counts()
            st.bar_chart(grade_counts)
        with col_chart2:
            st.markdown("**Students by Stream/House**")
            stream_counts = df['Stream'].value_counts()
            st.bar_chart(stream_counts)

elif page == "🔍 Search & Profiles":
    st.header("🔍 Search & Student Profiles")
    if df.empty:
        st.info("The student database is empty.")
    else:
        search_query = st.text_input("🔎 Search by First Name, Surname, or Admission Number:")
        
        filtered_df = df.copy()
        if search_query:
            filtered_df = filtered_df[
                filtered_df['Admission_No'].str.contains(search_query, case=False, na=False) |
                filtered_df['First_Name'].str.contains(search_query, case=False, na=False) |
                filtered_df['Surname'].str.contains(search_query, case=False, na=False)
            ]
            
        if filtered_df.empty:
            st.warning("No student matches your search query.")
        else:
            options_list = (filtered_df['First_Name'] + " " + filtered_df['Surname'] + " (" + filtered_df['Admission_No'] + ")").tolist()
            student_choice = st.selectbox("🎯 Select a Student to Open Full Profile Card", options_list)
            
            # Fetch details
            selected_adm = student_choice.split('(')[-1].replace(')', '').strip()
            student_data = df[df['Admission_No'] == selected_adm].iloc[0]
            
            st.markdown("---")
            st.subheader(f"👤 Profile Summary: {student_data['First_Name']} {student_data['Middle_Name'] if pd.notna(student_data['Middle_Name']) else ''} {student_data['Surname']}")
            
            p_col1, p_col2 = st.columns(2)
            with p_col1:
                st.markdown(f"**🔢 Admission Number:** {student_data['Admission_No']}")
                st.markdown(f"**🆔 UPI Number:** {student_data['UPI_Number']}")
                st.markdown(f"**🧬 Gender:** {student_data['Gender']}")
                st.markdown(f"**📅 Date of Birth:** {student_data['DOB']}")
                st.markdown(f"**🩺 Special Medical/Learning Needs:** {student_data['Special_Needs']}")
            with p_col2:
                st.markdown(f"**🏫 Grade Level:** {student_data['Grade_Level']}")
                st.markdown(f"**🛶 Stream / Class:** {student_data['Stream']}")
                st.markdown(f"**📜 Birth Certificate No:** {student_data['Birth_Cert_No']}")
                st.markdown(f"**👥 Parent's National ID:** {student_data['Parent_National_ID']}")
                st.markdown(f"**🟢 Current Status:** `{student_data['Status']}`")

elif page == "➕ Add New Student":
    st.header("➕ Register a New Student")
    with st.form("add_student_form", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            adm_no = st.text_input("Admission Number *")
            f_name = st.text_input("First Name *")
            m_name = st.text_input("Middle Name")
            l_name = st.text_input("Surname *")
            upi = st.text_input("UPI Number")
            dob = st.date_input("Date of Birth")
            gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        with col2:
            bc_no = st.text_input("Birth Certificate Number")
            grade = st.text_input("Grade Level (e.g., Grade 7)")
            stream = st.text_input("Stream (e.g., North)")
            special = st.text_input("Special Needs", value="None")
            parent_id = st.text_input("Parent's National ID")
            status = st.selectbox("Status", ["Active", "Inactive", "Suspended", "Transferred"])
            
        submitted = st.form_submit_button("📁 Save Student Profile")
        
        if submitted:
            if not adm_no or not f_name or not l_name:
                st.error("❌ Error: Please fill in all required fields marked with *")
            elif adm_no in df['Admission_No'].values:
                st.error(f"❌ Error: Admission Number '{adm_no}' already exists in the system!")
            else:
                new_student = {
                    'Admission_No': adm_no, 'First_Name': f_name, 'Middle_Name': m_name, 'Surname': l_name,
                    'UPI_Number': upi, 'DOB': str(dob), 'Gender': gender, 'Birth_Cert_No': bc_no,
                    'Grade_Level': grade, 'Stream': stream, 'Special_Needs': special,
                    'Parent_National_ID': parent_id, 'Birth_Cert_Image': '', 'Status': status
                }
                df = pd.concat([df, pd.DataFrame([new_student])], ignore_index=True)
                save_data(df)
                st.success(f"🎉 Success: {f_name} {l_name} has been successfully registered!")

elif page == "✏️ Edit Student Profile":
    st.header("✏️ Edit Existing Student Profile")
    if df.empty:
        st.info("The database is currently empty.")
    else:
        df['Full_Name'] = df['First_Name'] + " " + df['Surname'] + " (" + df['Admission_No'] + ")"
        edit_choice = st.selectbox("Select Student to Edit", df['Full_Name'].tolist())
        
        selected_adm = edit_choice.split('(')[-1].replace(')', '').strip()
        idx = df[df['Admission_No'] == selected_adm].index[0]
        student_data = df.loc[idx]
        
        with st.form("edit_student_form"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Editing Profile for Admission No:** `{student_data['Admission_No']}`")
                f_name = st.text_input("First Name", value=str(student_data['First_Name']))
                m_name = st.text_input("Middle Name", value=str(student_data['Middle_Name']) if pd.notna(student_data['Middle_Name']) else '')
                l_name = st.text_input("Surname", value=str(student_data['Surname']))
                upi = st.text_input("UPI Number", value=str(student_data['UPI_Number']) if pd.notna(student_data['UPI_Number']) else '')
                
                try:
                    current_dob = pd.to_datetime(student_data['DOB']).date()
                except:
                    import datetime
                    current_dob = datetime.date.today()
                dob = st.date_input("Date of Birth", value=current_dob)
                
                gender_list = ["Male", "Female", "Other"]
                g_idx = gender_list.index(student_data['Gender']) if student_data['Gender'] in gender_list else 0
                gender = st.selectbox("Gender", gender_list, index=g_idx)
            with col2:
                bc_no = st.text_input("Birth Certificate Number", value=str(student_data['Birth_Cert_No']) if pd.notna(student_data['Birth_Cert_No']) else '')
                grade = st.text_input("Grade Level", value=str(student_data['Grade_Level']) if pd.notna(student_data['Grade_Level']) else '')
                stream = st.text_input("Stream", value=str(student_data['Stream']) if pd.notna(student_data['Stream']) else '')
                special = st.text_input("Special Needs", value=str(student_data['Special_Needs']) if pd.notna(student_data['Special_Needs']) else 'None')
                parent_id = st.text_input("Parent's National ID", value=str(student_data['Parent_National_ID']) if pd.notna(student_data['Parent_National_ID']) else '')
                
                status_list = ["Active", "Inactive", "Suspended", "Transferred"]
                s_idx = status_list.index(student_data['Status']) if student_data['Status'] in status_list else 0
                status = st.selectbox("Status", status_list, index=s_idx)
                
            updated = st.form_submit_button("💾 Save Profile Changes")
            
            if updated:
                df.at[idx, 'First_Name'] = f_name
                df.at[idx, 'Middle_Name'] = m_name
                df.at[idx, 'Surname'] = l_name
                df.at[idx, 'UPI_Number'] = upi
                df.at[idx, 'DOB'] = str(dob)
                df.at[idx, 'Gender'] = gender
                df.at[idx, 'Birth_Cert_No'] = bc_no
                df.at[idx, 'Grade_Level'] = grade
                df.at[idx, 'Stream'] = stream
                df.at[idx, 'Special_Needs'] = special
                df.at[idx, 'Parent_National_ID'] = parent_id
                df.at[idx, 'Status'] = status
                
                save_data(df)
                st.success(f"🎉 Success: Updated details for {f_name} {l_name}!")
