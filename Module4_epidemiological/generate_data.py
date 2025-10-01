import pandas as pd
import numpy as np
from faker import Faker

# Set random seed for reproducibility
np.random.seed(42)
fake = Faker()
Faker.seed(42)

# Set population size
population_size = 1000

# Define street names for small rural town (Millbrook, NY)
street_names = [
    'Main Street', 'Church Street', 'Mill Road', 'Franklin Avenue',
    'Washington Street', 'Maple Avenue', 'Oak Lane', 'Pine Street',
    'Elm Street', 'Cedar Road', 'Meadow Lane', 'Hill Street',
    'Park Avenue', 'Route 44', 'Route 82', 'Chestnut Ridge Road'
]

# Generate addresses in Millbrook, NY
def generate_millbrook_address():
    street_number = np.random.randint(1, 500)
    street = np.random.choice(street_names)
    return f"{street_number} {street}, Millbrook, NY 12545"

# Generate all the fake data at once using list comprehensions
df = pd.DataFrame({
    'id': range(1, population_size + 1),
    'name': [fake.name() for _ in range(population_size)],
    'age': np.random.randint(18, 86, size=population_size),
    'gender': np.random.choice(['Male', 'Female'], size=population_size),
    'address': [generate_millbrook_address() for _ in range(population_size)],
    'is_smoker': np.random.choice([True, False], size=population_size),
    'at_risk': np.random.choice([True, False], size=population_size)
})

# Assign cancer based on smoking status
# For smokers: 20% chance, for non-smokers: 2% chance
cancer_probabilities = []
for smoker_status in df['is_smoker']:
    if smoker_status == True:
        cancer_probabilities.append(0.20)  # 20% chance for smokers
    else:
        cancer_probabilities.append(0.02)  # 2% chance for non-smokers

df['cancer_probability'] = cancer_probabilities
df['random_number'] = np.random.random(size=population_size)
df['has_cancer'] = df['random_number'] < df['cancer_probability']

# For people with cancer, randomly assign if it's a new or existing case
# Assume 60% are new cases, 40% are existing cases
df['is_new_case'] = False

new_case_assignments = []
people_with_cancer = df['has_cancer'].sum()

for i in range(people_with_cancer):
    random_value = np.random.random()
    if random_value < 0.60:
        new_case_assignments.append(True)
    else:
        new_case_assignments.append(False)

df.loc[df['has_cancer'] == True, 'is_new_case'] = new_case_assignments

# Drop the helper columns
df = df.drop(columns=['cancer_probability', 'random_number'])

# Save to CSV
df.to_csv('Module4_epidemiological/simulated_data.csv', index=False)
print(f"✓ Generated dataset with {len(df)} records")
print(f"✓ Saved to: Module4_epidemiological/simulated_data.csv")

