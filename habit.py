from datetime import date, timedelta


class Habit:
    def __init__(self, name):
        self.name = name
        self.completed_days = set()

    def mark_done(self, day=None):
        day = day or date.today()
        self.completed_days.add(day)

    def load_completed_days(self, days):
        from datetime import date
        self.completed_days = {date.fromisoformat(d) for d in days}

    def current_streak(self):
        if not self.completed_days:
            return 0

        streak = 0
        today = date.today()
        day = today

        while day in self.completed_days:
            streak += 1
            day -= timedelta(days=1)

        return streak

    def longest_streak(self):
        if not self.completed_days:
            return 0

        sorted_days = sorted(self.completed_days)
        longest = 1
        current = 1

        for i in range(1, len(sorted_days)):
            if sorted_days[i] == sorted_days[i - 1] + timedelta(days=1):
                current += 1
                longest = max(longest, current)
            else:
                current = 1

        return longest
