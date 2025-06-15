import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta

fake = Faker()

# Constants
NUM_RECORDS = 8950
GENDER_CHOICES = ['Female', 'Male']
GENDER_PROBS = [0.46, 0.54]

KENYAN_STATES_CITIES = {
    'Nairobi': ['Nairobi'],
    'Mombasa': ['Mombasa'],
    'Kisumu': ['Kisumu'],
    'Nakuru': ['Nakuru'],
    'Uasin Gishu': ['Eldoret'],
    'Kiambu': ['Thika', 'Ruiru'],
    'Machakos': ['Machakos', 'Athi River'],
    'Kajiado': ['Ngong', 'Kitengela'],
    'Meru': ['Meru'],
    'Nyeri': ['Nyeri']
}

YEARS_HIRE_PROBS = {year: prob for year, prob in zip(range(2015, 2025), np.random.dirichlet(np.ones(10), size=1)[0])}

DEPARTMENTS = {
    'HR': ['HR Manager', 'HR Assistant'],
    'Finance': ['Accountant', 'Finance Analyst'],
    'IT': ['Software Engineer', 'System Admin'],
    'Operations': ['Operations Manager', 'Clerk'],
    'Sales': ['Sales Executive', 'Sales Manager'],
    'Customer Service': ['Customer Rep', 'Call Center Agent']
}

DEPARTMENT_PROBS = [0.10, 0.15, 0.20, 0.20, 0.20, 0.15]

JOB_TITLE_PROBS = {
    'HR': [0.6, 0.4],
    'Finance': [0.7, 0.3],
    'IT': [0.75, 0.25],
    'Operations': [0.3, 0.7],
    'Sales': [0.5, 0.5],
    'Customer Service': [0.4, 0.6]
}

EDUCATION_MAPPING = {
    'HR Manager': 'Masters',
    'HR Assistant': 'Bachelors',
    'Accountant': 'Bachelors',
    'Finance Analyst': 'Masters',
    'Software Engineer': 'Bachelors',
    'System Admin': 'Bachelors',
    'Operations Manager': 'Masters',
    'Clerk': 'Diploma',
    'Sales Executive': 'Diploma',
    'Sales Manager': 'Bachelors',
    'Customer Rep': 'Diploma',
    'Call Center Agent': 'Diploma'
}

PERFORMANCE_CHOICES = ['Excellent', 'Good', 'Satisfactory', 'Needs Improvement']
PERFORMANCE_PROBS = [0.25, 0.40, 0.25, 0.10]

OVERTIME_CHOICES = ['Yes', 'No']
OVERTIME_PROBS = [0.30, 0.70]

SALARY_RANGES = {
    'HR Manager': (90000, 120000),
    'HR Assistant': (50000, 70000),
    'Accountant': (60000, 90000),
    'Finance Analyst': (70000, 110000),
    'Software Engineer': (80000, 130000),
    'System Admin': (60000, 100000),
    'Operations Manager': (85000, 120000),
    'Clerk': (40000, 60000),
    'Sales Executive': (45000, 70000),
    'Sales Manager': (70000, 100000),
    'Customer Rep': (35000, 50000),
    'Call Center Agent': (30000, 45000)
}

TERMINATION_PROB = 0.112
YEARS_TERM_PROBS = {year: prob for year, prob in zip(range(2015, 2025), np.random.dirichlet(np.ones(10), size=1)[0])}

EDUCATION_MULTIPLIERS = {
    'Diploma': 1.0,
    'Bachelors': 1.1,
    'Masters': 1.2
}
GENDER_ADJUSTMENTS = {'Male': 1.0, 'Female': 1.05}


# Utility functions
def generate_hire_date():
    year = random.choices(list(YEARS_HIRE_PROBS.keys()), weights=YEARS_HIRE_PROBS.values())[0]
    start = datetime(year, 1, 1)
    end = datetime(year, 12, 31)
    return fake.date_between(start, end)

def generate_birth_date(hire_date):
    age = random.randint(22, 60)
    birth_year = hire_date.year - age
    return fake.date_of_birth(minimum_age=22, maximum_age=60)

def generate_termination_date(hire_date):
    if random.random() > TERMINATION_PROB:
        return None
    year = random.choices(list(YEARS_TERM_PROBS.keys()), weights=YEARS_TERM_PROBS.values())[0]
    start = datetime(year, 1, 1)
    end = datetime(year, 12, 31)
    term_date = fake.date_between(start, end)
    # Ensure at least 6 months after hire
    if term_date < hire_date + timedelta(days=180):
        term_date = hire_date + timedelta(days=180)
    return term_date

def calculate_adjusted_salary(base_salary, gender, education_level, age):
    adj_salary = base_salary * GENDER_ADJUSTMENTS[gender] * EDUCATION_MULTIPLIERS[education_level]
    if age > 45:
        adj_salary *= 1.1
    return round(adj_salary, 2)

def get_city_state():
    state = random.choice(list(KENYAN_STATES_CITIES.keys()))
    city = random.choice(KENYAN_STATES_CITIES[state])
    return city, state

# Generate the dataset
records = []
for emp_id in range(1, NUM_RECORDS + 1):
    first_name = fake.first_name()
    last_name = fake.last_name()
    gender = random.choices(GENDER_CHOICES, weights=GENDER_PROBS)[0]
    city, state = get_city_state()
    hire_date = generate_hire_date()
    department = random.choices(list(DEPARTMENTS.keys()), weights=DEPARTMENT_PROBS)[0]
    job_title = random.choices(DEPARTMENTS[department], weights=JOB_TITLE_PROBS[department])[0]
    education_level = EDUCATION_MAPPING[job_title]
    performance_rating = random.choices(PERFORMANCE_CHOICES, weights=PERFORMANCE_PROBS)[0]
    overtime = random.choices(OVERTIME_CHOICES, weights=OVERTIME_PROBS)[0]
    base_salary = random.randint(*SALARY_RANGES[job_title])
    birth_date = generate_birth_date(hire_date)
    age = hire_date.year - birth_date.year
    termination_date = generate_termination_date(hire_date)
    adjusted_salary = calculate_adjusted_salary(base_salary, gender, education_level, age)

    records.append({
        'Employee ID': emp_id,
        'First Name': first_name,
        'Last Name': last_name,
        'Gender': gender,
        'City': city,
        'State': state,
        'Hire Date': hire_date,
        'Department': department,
        'Job Title': job_title,
        'Education Level': education_level,
        'Performance Rating': performance_rating,
        'Overtime': overtime,
        'Salary': base_salary,
        'Birth Date': birth_date,
        'Termination Date': termination_date,
        'Adjusted Salary': adjusted_salary
    })

# Create DataFrame
df_hr = pd.DataFrame(records)
print(df_hr.head())
# Save to CSV
df_hr.to_csv('hr_data.csv', index=False)