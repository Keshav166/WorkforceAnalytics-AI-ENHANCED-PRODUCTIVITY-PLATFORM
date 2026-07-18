"""
generate_sample_data.py
Generates a realistic synthetic employee productivity dataset matching the
schema this dashboard expects, for local development/demo purposes.

Run:  python data/generate_sample_data.py
Produces: data/employee_data.csv (10,000 rows)

Replace this file with your real "Extended Employee Performance and
Productivity" dataset at data/employee_data.csv — the dashboard does not
require this generator to run in production.
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

N = 10000

DEPARTMENTS = ["Engineering", "Sales", "Marketing", "HR", "Finance",
               "Operations", "Customer Support", "IT", "Legal", "R&D"]
JOB_TITLES = {
    "Engineering": ["Software Engineer", "Senior Engineer", "Engineering Manager", "QA Engineer"],
    "Sales": ["Sales Executive", "Account Manager", "Sales Manager", "Business Development Rep"],
    "Marketing": ["Marketing Analyst", "Content Strategist", "Marketing Manager", "SEO Specialist"],
    "HR": ["HR Generalist", "Recruiter", "HR Manager", "People Ops Analyst"],
    "Finance": ["Financial Analyst", "Accountant", "Finance Manager", "Auditor"],
    "Operations": ["Operations Analyst", "Ops Manager", "Logistics Coordinator", "Process Engineer"],
    "Customer Support": ["Support Agent", "Support Lead", "Customer Success Manager", "Technical Support"],
    "IT": ["IT Support", "Systems Administrator", "Network Engineer", "IT Manager"],
    "Legal": ["Legal Counsel", "Paralegal", "Compliance Officer", "Legal Manager"],
    "R&D": ["Research Scientist", "R&D Engineer", "Product Researcher", "Innovation Lead"],
}
EDUCATION_LEVELS = ["High School", "Bachelor", "Master", "PhD"]
GENDERS = ["Male", "Female", "Other"]
REMOTE_FREQ_OPTIONS = [0, 25, 50, 75, 100]

def random_dates(start, end, n):
    delta = (end - start).days
    return [start + timedelta(days=np.random.randint(0, delta)) for _ in range(n)]

departments = np.random.choice(DEPARTMENTS, N)
job_titles = [np.random.choice(JOB_TITLES[d]) for d in departments]
genders = np.random.choice(GENDERS, N, p=[0.52, 0.45, 0.03])
ages = np.random.randint(21, 60, N)
hire_dates = random_dates(datetime(2014, 1, 1), datetime(2025, 12, 31), N)
today = datetime(2026, 7, 18)
years_at_company = np.array([(today - d).days / 365.25 for d in hire_dates])
education = np.random.choice(EDUCATION_LEVELS, N, p=[0.15, 0.5, 0.28, 0.07])

satisfaction = np.clip(np.random.normal(6.8, 1.6, N), 1, 10)
training_hours = np.clip(np.random.normal(40, 20, N), 0, 150)
overtime_hours = np.clip(np.random.normal(8, 6, N), 0, 40)
projects = np.clip(np.random.poisson(6, N), 0, 25)
work_hours = np.clip(np.random.normal(42, 6, N), 30, 70)
sick_days = np.clip(np.random.poisson(4, N), 0, 30)
team_size = np.clip(np.random.normal(9, 4, N), 2, 30).astype(int)
remote_freq = np.random.choice(REMOTE_FREQ_OPTIONS, N, p=[0.3, 0.2, 0.2, 0.15, 0.15])
promotions = np.random.binomial(3, 0.2, N)

performance = (
    0.25 * (training_hours / 150 * 10)
    + 0.25 * (satisfaction)
    + 0.2 * (projects / 25 * 10)
    - 0.1 * (overtime_hours / 40 * 10)
    + np.random.normal(0, 1.2, N)
)
performance = np.clip((performance - performance.min()) / (performance.max() - performance.min()) * 9 + 1, 1, 10)

base_salary = 35000 + (years_at_company * 1800) + (performance * 3500)
edu_bonus = pd.Series(education).map({"High School": 0, "Bachelor": 4000, "Master": 9000, "PhD": 15000}).values
salary = np.clip(base_salary + edu_bonus + np.random.normal(0, 4000, N), 25000, 250000)

resign_prob = np.clip(0.35 - (satisfaction / 10 * 0.25) + (overtime_hours / 40 * 0.15), 0.02, 0.6)
resigned = np.random.binomial(1, resign_prob)

def perf_category(score):
    if score >= 8.5:
        return "Excellent"
    elif score >= 6.5:
        return "Good"
    elif score >= 4.5:
        return "Average"
    else:
        return "Needs Improvement"

def overtime_category(hours):
    if hours < 5:
        return "Low"
    elif hours < 15:
        return "Moderate"
    else:
        return "High"

df = pd.DataFrame({
    "Employee_ID": [f"EMP{100000 + i}" for i in range(N)],
    "Department": departments,
    "Gender": genders,
    "Age": ages,
    "Job_Title": job_titles,
    "Hire_Date": [d.strftime("%Y-%m-%d") for d in hire_dates],
    "Years_At_Company": np.round(years_at_company, 2),
    "Education_Level": education,
    "Performance_Score": np.round(performance, 2),
    "Monthly_Salary": np.round(salary, 2),
    "Work_Hours_Per_Week": np.round(work_hours, 1),
    "Projects_Handled": projects,
    "Overtime_Hours": np.round(overtime_hours, 1),
    "Sick_Days": sick_days,
    "Remote_Work_Frequency": remote_freq,
    "Team_Size": team_size,
    "Training_Hours": np.round(training_hours, 1),
    "Promotions": promotions,
    "Employee_Satisfaction_Score": np.round(satisfaction, 2),
    "Resigned": resigned,
})

df["Tenure_Years"] = df["Years_At_Company"]
df["Performance_Category"] = df["Performance_Score"].apply(perf_category)
df["Overtime_Category"] = df["Overtime_Hours"].apply(overtime_category)

df.to_csv("data/employee_data.csv", index=False)
print(f"Generated {len(df)} rows -> data/employee_data.csv")
