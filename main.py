# usaco training tracker
# stores problems in a local json file so you dont lose progress

import json
import os
from datetime import date

DATA_FILE = "usaco_data.json"

TOPICS = ["dp", "graphs", "greedy", "binary search", "sorting", "math", "trees", "brute force", "bfs/dfs", "other"]
DIFFICULTIES = ["bronze", "silver", "gold"]
SOURCES = ["usaco", "codeforces"]

# colors (just using ansi codes, no extra installs needed)
GREEN  = "\033[92m"
YELLOW = "\033[93m"
RED    = "\033[91m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(problems):
    with open(DATA_FILE, "w") as f:
        json.dump(problems, f, indent=2)

def log_problem(problems):
    print(f"\n{CYAN}--- Log a Problem ---{RESET}")

    name = input("Problem name: ").strip()
    if not name:
        print("Name cant be empty")
        return

    print("Difficulty: " + ", ".join(DIFFICULTIES))
    diff = input("Your choice: ").strip().lower()
    if diff not in DIFFICULTIES:
        print("Invalid difficulty")
        return

    print("Source: " + ", ".join(SOURCES))
    source = input("Your choice: ").strip().lower()
    if source not in SOURCES:
        print("Invalid source")
        return

    print("Topic: " + ", ".join(TOPICS))
    topic = input("Your choice: ").strip().lower()
    if topic not in TOPICS:
        topic = "other"

    time_str = input("How long did it take? (in minutes): ").strip()
    try:
        time_taken = int(time_str)
    except ValueError:
        print("Couldnt parse that, setting time to 0")
        time_taken = 0

    looked_up = input("Did you look up the solution? (y/n): ").strip().lower()
    needed_help = looked_up == "y"

    problem = {
        "name": name,
        "difficulty": diff,
        "source": source,
        "topic": topic,
        "time_minutes": time_taken,
        "needed_help": needed_help,
        "date": str(date.today())
    }

    problems.append(problem)
    save_data(problems)

    color = RED if needed_help else GREEN
    print(f"\n{color}Logged \"{name}\" ({diff} / {topic}){RESET}")

def show_stats(problems):
    if not problems:
        print("\nNo problems logged yet. Start solving!")
        return

    print(f"\n{CYAN}{BOLD}--- Your Stats ---{RESET}")
    print(f"Total problems solved: {BOLD}{len(problems)}{RESET}")

    # breakdown by difficulty
    for diff in DIFFICULTIES:
        count = len([p for p in problems if p["difficulty"] == diff])
        print(f"  {diff}: {count}")

    # help rate
    needed_help = [p for p in problems if p["needed_help"]]
    rate = round(len(needed_help) / len(problems) * 100)
    color = RED if rate > 50 else YELLOW if rate > 25 else GREEN
    print(f"\nLooked up solution: {color}{rate}%{RESET}")

    # avg solve time
    times = [p["time_minutes"] for p in problems if p["time_minutes"] > 0]
    if times:
        avg = round(sum(times) / len(times))
        print(f"Avg solve time: {avg} min")

    # weak topics (topics where you needed help most)
    print(f"\n{YELLOW}Weak spots (by help rate):{RESET}")
    topic_stats = {}
    for p in problems:
        t = p["topic"]
        if t not in topic_stats:
            topic_stats[t] = {"total": 0, "helped": 0}
        topic_stats[t]["total"] += 1
        if p["needed_help"]:
            topic_stats[t]["helped"] += 1

    # sort by help rate
    ranked = sorted(topic_stats.items(), key=lambda x: x[1]["helped"] / x[1]["total"], reverse=True)

    for topic, data in ranked:
        help_rate = round(data["helped"] / data["total"] * 100)
        bar = "#" * (help_rate // 10)
        color = RED if help_rate > 60 else YELLOW if help_rate > 30 else GREEN
        print(f"  {topic:<15} {color}{bar:<10}{RESET} {help_rate}% needed help  ({data['total']} solved)")

def list_problems(problems):
    if not problems:
        print("\nNothing logged yet")
        return

    print(f"\n{CYAN}--- Problem Log ---{RESET}")

    # optional filter
    filter_by = input("Filter by topic (leave blank for all): ").strip().lower()

    filtered = problems
    if filter_by:
        filtered = [p for p in problems if p["topic"] == filter_by]

    if not filtered:
        print("No problems found with that topic")
        return

    for p in filtered:
        help_tag = f"{RED}[looked up]{RESET}" if p["needed_help"] else f"{GREEN}[solved]{RESET}"
        diff_color = YELLOW if p["difficulty"] == "silver" else RED if p["difficulty"] == "gold" else RESET
        print(f"  {diff_color}{p['difficulty']:<8}{RESET} {p['name']:<30} {p['topic']:<15} {p['time_minutes']}min  {help_tag}  {p['date']}")

def show_menu():
    print(f"\n{BOLD}USACO Tracker{RESET}")
    print("1. log a problem")
    print("2. view stats")
    print("3. list problems")
    print("4. exit")

def main():
    problems = load_data()
    print(f"{CYAN}Welcome back! You have {len(problems)} problems logged.{RESET}")

    while True:
        show_menu()
        choice = input("\n> ").strip()

        if choice == "1":
            log_problem(problems)
        elif choice == "2":
            show_stats(problems)
        elif choice == "3":
            list_problems(problems)
        elif choice == "4":
            print("Good luck grinding!")
            break
        else:
            print("Invalid choice, pick 1-4")

main()
