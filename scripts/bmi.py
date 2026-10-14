

def classify_bmi(bmi):
    if bmi >= 30:
        category = "Obese"
    elif bmi >= 25:
        category = "Overweight"
    elif bmi >= 18.5:
        category = "Normal"
    else:
        category = "Underweight"
    print(category)  
   return(category)


bmi_value = 18 
result = classify_bmi(bmi_value)
print (f"Your category is {result}.")
#this bmi only refers to the bmi_value in line 1 