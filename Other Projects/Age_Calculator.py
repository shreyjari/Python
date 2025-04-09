from datetime import datetime

def calculate_age():
    try:
        # Prompt the user to input their birthdate
        birth_date = input("Enter your birthdate (YYYY-MM-DD): ")
        birth_date = datetime.strptime(birth_date, "%Y-%m-%d")

        # Get the current date
        today = datetime.today()

        # Calculate age
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

        # Display the age
        print(f"Your age is: {age} years")

    except ValueError:
        print("Invalid date format. Please use YYYY-MM-DD.")

# Run the age calculator
if __name__ == "__main__":
    calculate_age()


# def calculate_age2():
#     try:
#         # Prompt the user to input their birthdate
#         birth_year = input("Enter your birthyear (YYYY): ")

#         # Get the current year
#         current_year = datetime.today().year

#         # Calculate age
#         age = current_year - int(birth_year)

#         # Display the age
#         print(f"Your age is: {age} years")

#     except ValueError:
#         print("Invalid year format. Please use YYYY.")

# # Run the age calculator
# if __name__ == "__main__":
#     calculate_age2()
    
