from habit import Habit
from db import Database
from datetime import date


class HabitManager:
    def __init__(self):
        self.db = Database()
        self.habits = {}

        for name in self.db.get_habits():
            habit = Habit(name)
            logs = self.db.get_logs_for_habit(name)
            habit.load_completed_days(logs)
            self.habits[name] = habit

    def add_habit(self, name):
        if name in self.habits:
            print("Habit already exists")
            return

        self.db.add_habit(name)
        self.habits[name] = Habit(name)

    def delete_habit(self, name):
        if name not in self.habits:
            print("Habit not found")
            return

        self.db.delete_habit(name)
        del self.habits[name]
        print("Habit deleted")

    def get_habit(self, name):
        return self.habits.get(name)

    def list_habits(self):
        return list(self.habits.keys())

    def mark_done(self, name, day=None):
        habit = self.get_habit(name)

        if not habit:
            print("Habit not found")
            return

        actual_day = day or date.today()
        habit.mark_done(actual_day)
        self.db.add_log(name, actual_day.isoformat())


if __name__ == "__main__":
    m = HabitManager()

    while True:
        print("\n--- Habit Tracker ---")
        print("1. Add Habit")
        print("2. Mark Habit Done")
        print("3. View All Habits")
        print("4. View Streak")
        print("5. View 6-Month Stats")
        print("6. Delete Habit")
        print("7. Show 6-Month Graph")
        print("8. Heatmap (Last 3 Months)")
        print("9. Exit")

        choice = input("Choose option: ")

        if choice == "1":
            name = input("Enter habit name: ")
            m.add_habit(name)

        elif choice == "2":
            name = input("Enter habit name: ")
            m.mark_done(name)

        elif choice == "3":
            print("Habits:", m.list_habits())

        elif choice == "4":
            name = input("Enter habit name: ")
            habit = m.get_habit(name)
            if habit:
                print("Current streak:", habit.current_streak())
                print("Longest streak:", habit.longest_streak())
            else:
                print("Habit not found")

        elif choice == "5":
            name = input("Enter habit name: ")
            habit = m.get_habit(name)
            if habit:
                stats = habit.stats_last_6_months()
                print("Total completed (6 months):", stats["total_completed"])
                print("Consistency:", stats["consistency_percent"], "%")
            else:
                print("Habit not found")

        elif choice == "6":
            name = input("Enter habit name to delete: ")
            m.delete_habit(name)

        elif choice == "7":
            name = input("Enter habit name: ")
            habit = m.get_habit(name)
            if habit:
                habit.plot_last_6_months()
            else:
                print("Habit not found")

        elif choice == "8":
            name = input("Enter habit name: ")
            habit = m.get_habit(name)

            if habit:
                habit.heatmap_last_3_months()
            else:
                print("Habit not found")

        elif choice == "9":
            print("Goodbye 👋")
            break

        else:
            print("Invalid choice")