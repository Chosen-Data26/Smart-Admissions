import random
import pandas as pd

# Faculties and departments
departments = {
    "Arts": [
        "Foreign Languages", "English Language", "English Literature",
        "Linguistics", "Philosophy", "History and International studies",
        "Creative Arts: Visual", "Creative Arts: Theatre", "Creative Arts: Music"
    ],
    "Social Sciences": [
        "Economics", "Political Science", "Geography and Planning",
        "Social Work", "Psychology", "Criminology", "Sociology",
        "Public Affairs", "Transport Planning"
    ],
    "Management Sciences": [
        "Business Administration", "Industrial Relations", "Insurance",
        "Accounting", "Banking and Finance", "Project Management",
        "Marketing", "Public Administration"
    ],
    "Law": [
        "Jurisprudence and International Law", "Commercial and Industrial Law", "Public Law",
        "Islamic Law", "Private and Property Law", "Legal Studies"
    ],
    "Science": [
        "Mathematics", "Physics", "Chemistry", "Computer Science", "Zoology", "Fisheries",
        "Botany", "Microbiology"
    ],
    "Engineering": [
        "Chemical and Polymer Engineering", "Electronic and Computer Engineering", 
        "Mechanical Engineering", "Aeronautical and Astronautical Engineering",
        "Civil Engineering", "Industrial Engineering"
    ],
    "Clinical Science": [
        "Medicine and Surgery", "Dentistry", "Pharmacology", "Nursing"
    ]
}

# o'level grading scale
olevel_scale = {
     'A1': 10, 'B1': 8, 'B2': 7, 'B3': 6,
    'C1': 5, 'C2': 4, 'C3': 3, 'C4': 2,
    'C5': 1, 'C6': 0
}

# Simulate dataset
num_applicants = 1000
data = []

for _ in range(num_applicants):
    faculty = random.choice(list(departments.keys()))
    department = random.choice(departments[faculty])
    
    #Simulate UTME score
    utme_score = random.randint(120, 400)
    
    #Simulate O'level grades and score
    grades = random.choices (list(olevel_scale.keys()), k=5)
    olevel_points = [olevel_scale[g] for g in grades]
    olevel_avg = sum(olevel_points)

    #screening score calculation: 50% UTME + 50% O'level
    screening_score = round((utme_score / 8) + sum(olevel_points), 2)
    
    #O'level passed (assume pass if no F9 or more than 2 sittings)
    olevel_passed = all(score > 0 for score in olevel_points)
    
    # Admission logic
    if utme_score >= 195 and screening_score >= 50 and olevel_passed:
        admitted = 1
    else:
        admitted = 0
    
    data.append([
        faculty, department, utme_score, screening_score, olevel_passed, admitted, ", ".join(grades)
    ])

# Create dataframe
df = pd.DataFrame(data, columns=[
    "faculty", "department", "utme_score",
    "screening_score", "olevel_passed", "admitted", "olevel_grades"
])

# Save to CSV
import os
import pandas as pd
import random

# ... your data generation code ...

# Construct full path to save the file reliably
base_dir = os.path.dirname(os.path.dirname(__file__))  # this gets to Smart-Admissions/
data_path = os.path.join(base_dir, "Data", "smart_admission_data.csv")
df.to_csv(data_path, index=False)

print("Dataset generated successfully!")
