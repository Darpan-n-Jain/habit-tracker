from habit import Habit
from db import Database
from datetime import date


class HabitManager:
    def __init__(self):
        self.db = Database()
        self.habits = {}

        # Load habits from DB
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


# ---------------- TEST ----------------
if __name__ == "__main__":
    m = HabitManager()

    while True:
        print("\n--- Habit Tracker ---")
        print("1. Add Habit")
        print("2. Mark Habit Done")
        print("3. View All Habits")
        print("4. View Streak")
        print("5. Exit")

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
            print("Goodbye 👋")
            break

        else:
            print("Invalid choice")
