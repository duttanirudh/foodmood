import csv
import math
import matplotlib.pyplot as plt
from datetime import datetime


food_data = {
    "roti": {"protein": 3, "carbs": 15, "fat": 1, "fiber": 2},
    "rice": {"protein": 2.5, "carbs": 28, "fat": 0.3, "fiber": 0.4},
    "dal": {"protein": 9, "carbs": 27, "fat": 0.4, "fiber": 5},
    "paneer": {"protein": 18, "carbs": 1.2, "fat": 20, "fiber": 0},
    "chicken": {"protein": 27, "carbs": 0, "fat": 3, "fiber": 0},
    "vegetables": {"protein": 2, "carbs": 8, "fat": 0.2, "fiber": 3},
    "milk": {"protein": 3.4, "carbs": 5, "fat": 4, "fiber": 0},
    "banana": {"protein": 1.3, "carbs": 27, "fat": 0.3, "fiber": 3}
}

def initialize_file():
    try:
        with open("nutrimind_data.csv", "x", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([
                "Date", "Protein", "Carbs", "Fat", "Fiber",
                "Sleep", "Water", "Mood"
            ])
    except FileExistsError:
        pass


def log_daily_entry():
    print("\n--- Daily Nutrition & Mood Entry ---")

    date = input("Enter date (DD-MM-YYYY): ")
    try:
        datetime.strptime(date, "%d-%m-%Y")
    except ValueError:
        print("Invalid date format.")
        return

    foods = input("Enter foods eaten (comma separated): ").lower().split(",")

    total_protein = total_carbs = total_fat = total_fiber = 0
    valid_foods = 0

    for food in foods:
        food = food.strip()
        if food in food_data:
            data = food_data[food]
            total_protein += data["protein"]
            total_carbs += data["carbs"]
            total_fat += data["fat"]
            total_fiber += data["fiber"]
            valid_foods += 1

    if valid_foods == 0:
        print("No valid food items found.")
        return

    sleep = float(input("Enter sleep hours: "))
    water = float(input("Enter water intake (litres): "))
    mood = int(input("Enter mood (1–10): "))

    with open("nutrimind_data.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([
            date,
            round(total_protein, 2),
            round(total_carbs, 2),
            round(total_fat, 2),
            round(total_fiber, 2),
            sleep,
            water,
            mood
        ])

    print("Entry saved successfully.")


def load_data():
    data = {
        "protein": [],
        "carbs": [],
        "fat": [],
        "fiber": [],
        "sleep": [],
        "water": [],
        "mood": []
    }

    with open("nutrimind_data.csv", "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data["protein"].append(float(row["Protein"]))
            data["carbs"].append(float(row["Carbs"]))
            data["fat"].append(float(row["Fat"]))
            data["fiber"].append(float(row["Fiber"]))
            data["sleep"].append(float(row["Sleep"]))
            data["water"].append(float(row["Water"]))
            data["mood"].append(int(row["Mood"]))

    return data


def calculate_correlation(x, y):
    n = len(x)
    mean_x = sum(x) / n
    mean_y = sum(y) / n

    numerator = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
    denominator = math.sqrt(
        sum((x[i] - mean_x) ** 2 for i in range(n)) *
        sum((y[i] - mean_y) ** 2 for i in range(n))
    )

    if denominator == 0:
        return 0

    return round(numerator / denominator, 2)


def analyze_data():
    data = load_data()
    mood = data["mood"]

    print("\n--- Correlation Analysis ---")
    for key in data:
        if key != "mood":
            r = calculate_correlation(data[key], mood)
            print(f"{key.capitalize()} vs Mood: {r}")


def plot_trends():
    data = load_data()
    days = list(range(1, len(data["mood"]) + 1))

    plt.figure()
    plt.plot(days, data["mood"], label="Mood")
    plt.plot(days, data["protein"], label="Protein")
    plt.plot(days, data["fiber"], label="Fiber")
    plt.xlabel("Days")
    plt.ylabel("Value")
    plt.title("Mood vs Nutrition Trends")
    plt.legend()
    plt.show()



def main():
    initialize_file()

    while True:
        print("\n==== NutriMind Menu ====")
        print("1. Log daily entry")
        print("2. Analyze correlations")
        print("3. Plot trends")
        print("4. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            log_daily_entry()
        elif choice == "2":
            analyze_data()
        elif choice == "3":
            plot_trends()
        elif choice == "4":
            print("Exiting NutriMind.")
            break
        else:
            print("Invalid choice.")



main()



