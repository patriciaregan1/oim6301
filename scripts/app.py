#import bmi 

#result = bmi.compute_bmi(70,1.75) 
#print(f"Computed BMI is {result:.2f}")

people = [
    {"name": "Alice", "height": 1.65, "weight": 60},
    {"name": "Bob", "height": 1.80, "weight": 85},
    {"name": "Charlie", "height": 1.75, "weight": 78},
    {"name": "Diana", "height": 1.70, "weight": 65},
    {"name": "Ethan", "height": 1.78, "weight": 90},
    {"name": "Fiona", "height": 1.60, "weight": 55},
    {"name": "George", "height": 1.85, "weight": 95},
    {"name": "Hannah", "height": 1.68, "weight": 62},
] 

for person in people: 
    print(person) 
