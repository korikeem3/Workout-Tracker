from db import create_tables
from services.user_service import create_user, get_user_by_username
from services.workout_service import (
    create_workout_entry,
    get_workout_history_by_user,
    update_workout_entry,
    delete_workout_entry
)
#from services.strength_service import compare_to_population, get_user_best_for_exercise

def main():
    # 1. Create the tables if they don't exist
    create_tables()

    print("Welcome to the Workout Tracker App!")

    while True:
        print("\nWhat would you like to do?")
        print("1. Sign Up")
        print("2. Log In")
        print("3. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            username = input("Enter a username: ")
            password = input("Enter a password: ")
            user_id = create_user(username, password)
            if user_id:
                print(f"User '{username}' created with user_id = {user_id}")
            else:
                print("Error creating user. Possibly username taken.")
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")

            user_data = get_user_by_username(username)
            if user_data and user_data['password'] == password:
                print(f"Login successful! Welcome, {username}.")
                user_menu(user_data['id'])
            else:
                print("Invalid username or password.")
        elif choice == "3":
            print("Exiting... Goodbye!")
            break
        else:
            print("Invalid choice, try again.")

def user_menu(user_id):
    """
    Menu shown to a user after logging in successfully.
    """
    while True:
        print("\nUser Menu:")
        print("1. Create Workout Entry")
        print("2. View Workout History")
        print("3. Update a Workout Entry")
        print("4. Delete a Workout Entry")
        print("5. Compare Strength to Population")
        print("6. Logout")

        choice = input("Enter choice: ")

        if choice == "1":
            exercise = input("Enter exercise name: ")
            weight = int(input("Enter weight lifted (lbs): "))
            reps = int(input("Enter number of repetitions: "))
            sets = int(input("Enter number of sets: "))

            entry_id = create_workout_entry(user_id, exercise, weight, reps, sets)
            if entry_id:
                print(f"Workout entry created with ID: {entry_id}")
            else:
                print("Error creating workout entry.")
        elif choice == "2":
            history = get_workout_history_by_user(user_id)
            if not history:
                print("No workouts found.")
            else:
                for w in history:
                    print(f"ID={w['workout_id']} | {w['exercise']} | "
                          f"Weight: {w['weight']} | Reps: {w['reps']} | Sets: {w['sets']} | Date: {w['date']}")
        elif choice == "3":
            workout_id = int(input("Enter the workout entry ID to update: "))
            exercise = input("Enter the new exercise name (or leave blank): ")
            weight_str = input("Enter the new weight (or leave blank): ")
            reps_str = input("Enter the new reps (or leave blank): ")
            sets_str = input("Enter the new sets (or leave blank): ")

            exercise = exercise if exercise else None
            weight = int(weight_str) if weight_str else None
            reps = int(reps_str) if reps_str else None
            sets = int(sets_str) if sets_str else None

            update_workout_entry(workout_id, exercise, weight, reps, sets)
            print("Workout entry updated.")
        elif choice == "4":
            workout_id = int(input("Enter the workout entry ID to delete: "))
            delete_workout_entry(workout_id)
            print("Workout entry deleted.")
        # elif choice == "5":
        #     exercise = input("Enter exercise name to compare (e.g. 'Bench Press'): ")
        #     history = get_workout_history_by_user(user_id)
        #     user_best = get_user_best_for_exercise(user_id, exercise, history)
        #     if user_best == 0:
        #         print(f"You have no recorded {exercise} workouts.")
        #     else:
        #         comparison = compare_to_population(exercise, user_best)
        #         print(comparison)
        elif choice == "6":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
