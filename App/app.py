import streamlit as st
import pandas as pd
import joblib
import os
import base64

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded_string = base64.b64encode(img_file.read()).decode()
    return encoded_string


# --- Set page config ---
st.set_page_config(page_title="LASU Smart Admission Predictor", page_icon="🎓", layout="centered")

# A little background CSS
st.markdown("""
    <style>
        .stApp {
            background-color: #f5f9ff;
            background-image: linear-gradient(to bottom right, #f5f9ff, #dbe9ff);
        }
    </style>
""", unsafe_allow_html=True)

# --- Title & Intro ---
st.markdown("<h1 style='text-align: center; color: navy;'>🎓 LASU Smart Admission Predictor</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Check your admission chances based on your UTME, Screening, and O'Level scores.</p>", unsafe_allow_html=True)
st.write("---")

# --- Load model and encoders ---
base_dir = os.path.join("..", "Notebooks", "Model")
model = joblib.load(os.path.join(base_dir, "smart_admission_model.pkl"))
faculty_encoder = joblib.load(os.path.join(base_dir, "faculty_encoder.pkl"))
department_encoder = joblib.load(os.path.join(base_dir, "department_encoder.pkl"))

# --- User Inputs ---
col1, col2 = st.columns(2)

with col1:
    faculty = st.selectbox("📚 Select Faculty", sorted(list(faculty_encoder.classes_)))
    utme_score = st.slider("📝 UTME Score (out of 400)", 0, 400, 200)

with col2:
    department = st.selectbox("🏛️ Select Department", sorted(list(department_encoder.classes_)))
    screening_score = st.slider("📊 Screening Score (out of 100)", 0, 100, 50)

# --- O'Level Grades Section ---
st.markdown("### 🧾 Enter O'Level Grades (English is compulsory)")
st.markdown("*English is compulsory. Then enter 4 other required subjects with their grades.*")

grades_map = {
    "A1": 1, "B2": 2, "B3": 3, "C4": 4, "C5": 5, "C6": 6,
    "D7": 7, "E8": 8, "F9": 9
}

# ✅ Define lists before using them
subject_grades = []
all_subjects = []

# English (Compulsory)
col1, col2 = st.columns([2, 1])
with col1:
    english_subject = "English Language"
    st.text_input("Subject 1", value=english_subject, disabled=True)
    all_subjects.append(english_subject)
with col2:
    eng_grade_input = st.selectbox("Grade for English", list(grades_map.keys()), key="grade_eng")
eng_grade = grades_map[eng_grade_input]
subject_grades.append(eng_grade)

# Subjects 2 to 5 (User-defined)
for i in range(2, 6):
    col1, col2 = st.columns([2, 1])
    with col1:
        subject_name = st.text_input(f"Subject {i} Name", key=f"subject_{i}")
        all_subjects.append(subject_name)
    with col2:
        grade_input = st.selectbox("Grade", list(grades_map.keys()), key=f"grade_{i}")
    grade_value = grades_map[grade_input]
    subject_grades.append(grade_value)

# ✅ Check O'Level pass condition (C6 and above in all 5)
olevel_passed = int(all(g <= 6 for g in subject_grades))

# 📘 Show subject & grade summary
if st.checkbox("Show entered subjects and grades"):
    st.markdown("### 📘 Subject Grades Summary")
    for subj, grade_key in zip(all_subjects, ["grade_eng", "grade_2", "grade_3", "grade_4", "grade_5"]):
        grade = st.session_state.get(grade_key, "N/A")
        st.write(f"- {subj}: {grade}")

# --- Predict Admission ---
if st.button("🔍 Predict Admission"):
    try:
        # Encode faculty and department
        faculty_encoded = faculty_encoder.transform([faculty])[0]
        department_encoded = department_encoder.transform([department])[0]

        # Prepare input DataFrame
        input_df = pd.DataFrame([{
            "faculty_encoded": faculty_encoded,
            "department_encoded": department_encoded,
            "utme_score": utme_score,
            "utme_scaled": utme_score / 400,
            "screening_score": screening_score,
            "screening_scaled": screening_score / 100,
            "olevel_passed": olevel_passed
        }])

        # Make prediction
        prediction = model.predict(input_df)[0]
        probability = model.predict_proba(input_df)[0][1]

        # --- Display Results ---
        st.write("---")
        if prediction == 1:
            st.success("🎉 You are likely to be ADMITTED!")
        else:
            st.error("❌ You may NOT be admitted.")

        st.info(f"🎯 Admission Probability: **{round(probability * 100, 2)}%**")

    except Exception as e:
        st.error(f"An error occurred: {e}")

