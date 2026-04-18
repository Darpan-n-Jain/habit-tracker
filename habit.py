from datetime import date, timedelta


class Habit:
    def __init__(self, name):
        self.name = name
        self.completed_days = set()

    def mark_done(self, day=None):
        day = day or date.today()
        self.completed_days.add(day)

    def load_completed_days(self, days):
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

    def plot_last_6_months(self):
        import matplotlib.pyplot as plt

        today = date.today()
        six_months_ago = today - timedelta(days=180)

        days_range = []
        completion = []

        current = six_months_ago
        while current <= today:
            days_range.append(current)
            completion.append(1 if current in self.completed_days else 0)
            current += timedelta(days=1)

        plt.figure()
        plt.plot(days_range, completion)
        plt.title(f"{self.name} - Last 6 Months Activity")
        plt.xlabel("Date")
        plt.ylabel("Completed (1=yes, 0=no)")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    def pie_chart_last_30_days(self):
        import matplotlib.pyplot as plt

        today = date.today()
        start = today - timedelta(days=30)

        done = 0
        missed = 0

        current = start
        while current <= today:
            if current in self.completed_days:
                done += 1
            else:
                missed += 1
            current += timedelta(days=1)

        labels = ["Done", "Missed"]
        values = [done, missed]
        colors = ["#4CAF50", "#F44336"]

        plt.figure()
        plt.pie(
            values,
            labels=labels,
            colors=colors,
            autopct="%1.0f days",
            startangle=90
        )

        plt.title(f"{self.name} - Last 30 Days")
        plt.axis("equal")
        plt.show()
        
        
    def heatmap_last_3_months(self):
        import matplotlib.pyplot as plt
        import numpy as np
        from datetime import date, timedelta
        from matplotlib.colors import ListedColormap

        today = date.today()
        start = today - timedelta(days=90)

        days = []
        current = start
        while current <= today:
            days.append(current)
            current += timedelta(days=1)

        weeks = len(days) // 7 + 1
        data = np.zeros((7, weeks))

        for d in days:
            week = (d - start).days // 7
            weekday = d.weekday()

            if d in self.completed_days:
                data[weekday][week] = 1

        # GitHub style colors
        cmap = ListedColormap(["#ebedf0", "#2ecc71"])

        fig, ax = plt.subplots(figsize=(14, 4))
        ax.imshow(data, cmap=cmap, aspect="equal")

        # create spacing between squares
        ax.set_xticks(np.arange(-.5, weeks, 1), minor=True)
        ax.set_yticks(np.arange(-.5, 7, 1), minor=True)
        ax.grid(which="minor", color="white", linestyle='-', linewidth=2)

        ax.tick_params(which="minor", bottom=False, left=False)

        # weekday labels
        ax.set_yticks(range(7))
        ax.set_yticklabels(["Mon","Tue","Wed","Thu","Fri","Sat","Sun"])

        # month labels
        month_positions = []
        month_labels = []

        for d in days:
            if d.day == 1:
                week = (d - start).days // 7
                month_positions.append(week)
                month_labels.append(d.strftime("%b"))

        ax.set_xticks(month_positions)
        ax.set_xticklabels(month_labels)

        # remove outer border
        for spine in ax.spines.values():
            spine.set_visible(False)

        ax.set_title(f"{self.name} Habit Heatmap (Last 3 Months)", fontsize=12)

        plt.tight_layout()
        plt.show()