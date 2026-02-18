# ============================================================
# Healthy Habits Tracker
# Features: multi-entry tracking, time-of-day, upper bound
# validation, inline entry deletion, and end-of-day reset.
# ============================================================

# --- Valid time-of-day options ---
TIME_SLOTS: tuple[str, ...] = ("morning", "afternoon", "evening")

# --- Habit configuration — single source of truth ---
# max_value: upper bound per single entry (e.g. can't sleep > 24 hrs)
# entries:   populated at runtime, starts empty each session
HABITS: dict[str, dict] = {
    "Water Intake": {"unit": "cups",    "threshold": 8,  "max_value": 20,  "entries": []},
    "Exercise":     {"unit": "minutes", "threshold": 30, "max_value": 300, "entries": []},
    "Sleep":        {"unit": "hours",   "threshold": 7,  "max_value": 24,  "entries": []},
}


# ------------------------------------------------------------
# INPUT HELPERS
# ------------------------------------------------------------

def get_positive_float(prompt: str, max_value: float) -> float | None:
    """
    Prompts for a numeric value between 0 and max_value (inclusive).
    Returns float if valid, None if user types 'done' or presses Enter.
    """
    while True:
        raw = input(prompt).strip()

        if raw.lower() in ("done", "d", ""):
            return None

        try:
            value = float(raw)

            if value < 0:
                print("  ⚠  Value must be 0 or greater. Try again.")
                continue

            if value > max_value:
                print(f"  ⚠  Value cannot exceed {max_value}. Try again.")
                continue

            return value

        except ValueError:
            print("  ⚠  Invalid input. Please enter a number (or 'done' to finish).")


def get_time_of_day() -> str:
    """
    Prompts for morning / afternoon / evening.
    Loops until a valid option is entered.
    """
    options_str = " / ".join(TIME_SLOTS)

    while True:
        raw = input(f"  Time of day ({options_str}): ").strip().lower()

        if raw in TIME_SLOTS:
            return raw

        print(f"  ⚠  Please enter one of: {options_str}")


# ------------------------------------------------------------
# DISPLAY HELPER
# ------------------------------------------------------------

def show_entries(entries: list[dict], unit: str) -> None:
    """
    Prints all current entries with a 1-based index number.

    Example output:
        Current entries:
          [1] Morning    — 2.5 cups
          [2] Afternoon  — 1.0 cups
    """
    if not entries:
        print("  (no entries yet)")
        return

    print("  Current entries:")
    for i, entry in enumerate(entries, start=1):
        print(f"    [{i}] {entry['time'].capitalize():<12} — {entry['value']:.1f} {unit}")


# ------------------------------------------------------------
# DELETION HELPER
# ------------------------------------------------------------

def delete_entry(entries: list[dict], unit: str) -> None:
    """
    Shows current entries and asks the user which index to delete.
    Mutates the entries list in place — no return value needed.
    """
    if not entries:
        print("  ⚠  No entries to delete.")
        return

    show_entries(entries, unit)

    while True:
        raw = input(f"  Enter entry number to delete (1-{len(entries)}): ").strip()

        try:
            index = int(raw)

            if index < 1 or index > len(entries):
                print(f"  ⚠  Please enter a number between 1 and {len(entries)}.")
                continue

            # pop(index - 1): convert 1-based user input to 0-based list index
            removed = entries.pop(index - 1)
            print(f"  ✅ Deleted: {removed['time'].capitalize()} — {removed['value']:.1f} {unit}")
            break

        except ValueError:
            print("  ⚠  Invalid input. Please enter a number.")


# ------------------------------------------------------------
# RESET HELPER
# ------------------------------------------------------------

def clear_all_entries() -> None:
    """
    Resets all habit entries to empty lists.
    Mutates the HABITS dict in place — iterates every habit and
    reassigns its 'entries' key to a fresh empty list.

    Called at end-of-day so the user starts clean the next day.
    Does NOT reset thresholds or config — only the tracked data.
    """
    for config in HABITS.values():
        # Reassign to a new empty list — cleanly wipes all entries
        # HABITS.values() gives us the inner config dicts directly,
        # so we can modify them without needing the habit name key
        config["entries"].clear()

    print("\n  ✅ All entries cleared. Ready for a new day!")
    print(f"  Habits reset: {', '.join(HABITS.keys())}")


# ------------------------------------------------------------
# COLLECTION
# ------------------------------------------------------------

def collect_entries(habit_name: str, unit: str, max_value: float) -> list[dict]:
    """
    Collects entries for a single habit with an inline action menu.

        [A]dd  [D]elete  [V]iew  [Q]uit

    Returns the final list[dict] of entries when user quits.
    """
    entries: list[dict] = []

    print(f"\n--- {habit_name} Tracker ({unit}) ---")
    print(f"  Valid range per entry: 0 - {max_value} {unit}")

    while True:
        print("\n  What would you like to do?")
        print("    [A] Add entry")
        print("    [D] Delete entry")
        print("    [V] View entries")
        print("    [Q] Done with this habit")

        choice = input("  Choice: ").strip().lower()

        if choice == "a":
            value = get_positive_float(f"  Value ({unit}): ", max_value)
            if value is None:
                continue
            time_of_day = get_time_of_day()
            entries.append({"value": value, "time": time_of_day})
            print(f"  ✅ Added: {time_of_day.capitalize()} — {value:.1f} {unit}")

        elif choice == "d":
            delete_entry(entries, unit)

        elif choice == "v":
            show_entries(entries, unit)

        elif choice == "q":
            print(f"\n  Final entries for {habit_name}:")
            show_entries(entries, unit)
            break

        else:
            print("  ⚠  Please enter A, D, V, or Q.")

    return entries


# ------------------------------------------------------------
# EVALUATION
# ------------------------------------------------------------

def evaluate_habit(habit_name: str, entries: list[dict], threshold: float, unit: str) -> float:
    """
    Sums entries, compares against threshold, prints result with breakdown.
    Returns the total so the caller can use it for cross-habit aggregation.
    """
    total = sum(entry["value"] for entry in entries)

    if total >= threshold:
        print(f"  ✅ {habit_name}: {total:.1f} {unit} — Goal met! (Target: {threshold} {unit})")
    else:
        shortfall = threshold - total
        print(f"  ❌ {habit_name}: {total:.1f} {unit} — {shortfall:.1f} {unit} below target (Target: {threshold} {unit})")

    if entries:
        for entry in entries:
            print(f"      {entry['time'].capitalize():<12} — {entry['value']:.1f} {unit}")

    return total



# ------------------------------------------------------------
# TOTALS AND AVERAGES
# ------------------------------------------------------------

def show_totals_and_averages(totals: dict[str, float]) -> None:
    """
    Prints a footer table showing total and average per-entry for each habit.

    totals: dict of {habit_name: total_value} — passed in from show_summary()
            so this function stays pure (no direct HABITS access needed).

    Average is calculated as:
        total / number_of_entries  — if entries exist
        0.0                        — if no entries (avoids ZeroDivisionError)

    Example output:
        Habit            Total       Avg/Entry
        ----------------------------------------
        Water Intake     5.0 cups    2.5 cups
        Exercise         35.0 min    17.5 min
        Sleep            7.0 hrs     7.0 hrs
    """
    print("-" * 50)
    print(f"  {'Habit':<16} {'Total':<14} {'Avg/Entry'}")
    print(f"  {'-'*16} {'-'*13} {'-'*12}")

    for habit_name, config in HABITS.items():
        total     = totals[habit_name]
        unit      = config["unit"]
        entries   = config["entries"]
        count     = len(entries)

        # Ternary expression: value_if_true if condition else value_if_false
        # Avoids ZeroDivisionError when no entries were logged
        average = total / count if count > 0 else 0.0

        print(f"  {habit_name:<16} {total:<6.1f} {unit:<8} {average:.1f} {unit}")

    print("-" * 50)
    print(f"  Total entries logged today: {sum(len(c['entries']) for c in HABITS.values())}")


# ------------------------------------------------------------
# DAILY SUMMARY
# ------------------------------------------------------------

def show_summary() -> None:
    """
    Evaluates all habits and prints the daily summary.
    Collects the total returned by evaluate_habit() for each habit,
    then passes them to show_totals_and_averages() for the footer.
    """
    print("\n" + "=" * 50)
    print("           📊 Daily Summary")
    print("=" * 50)

    # Collect each habit's total as evaluate_habit() runs
    # totals is built as a dict: {"Water Intake": 5.0, "Exercise": 35.0, ...}
    totals: dict[str, float] = {}

    for habit_name, config in HABITS.items():
        totals[habit_name] = evaluate_habit(
            habit_name,
            config["entries"],
            config["threshold"],
            config["unit"]
        )
        print()

    # Print totals and averages footer using collected totals
    show_totals_and_averages(totals)
    print("=" * 50)


# ------------------------------------------------------------
# ORCHESTRATION
# ------------------------------------------------------------

def run_tracker() -> None:
    """
    Runs one tracking session — collects entries for all habits
    then shows the daily summary.
    """
    print("\n" + "=" * 50)
    print("       🌿 Healthy Habits Tracker 🌿")
    print("=" * 50)

    # --- DEBUG: Confirm config loaded ---
    print(f"[DEBUG] Habits: {list(HABITS.keys())}")
    print(f"[DEBUG] Max values: { {k: v['max_value'] for k, v in HABITS.items()} }")

    # Collect entries for each habit
    for habit_name, config in HABITS.items():
        config["entries"] = collect_entries(
            habit_name,
            config["unit"],
            config["max_value"]
        )

    # --- DEBUG: Confirm final structured data ---
    for name, cfg in HABITS.items():
        print(f"[DEBUG] {name}: {cfg['entries']}")

    # Show summary after all habits are tracked
    show_summary()
    print("  Keep it up! Small habits compound over time. 💪")
    print("=" * 50)


def main() -> None:
    """
    Outer application loop — the main menu.

    Wraps run_tracker() so the app stays alive after a session ends.
    The user can:
        [T] Track habits for today
        [S] View current summary
        [R] Reset / clear all entries (end of day)
        [Q] Quit the application

    This separation means run_tracker() stays focused on one session,
    while main() handles the application lifecycle — same pattern as
    a controller calling a service in Spring.
    """
    print("=" * 50)
    print("   🌿 Welcome to Healthy Habits Tracker 🌿")
    print("=" * 50)

    while True:
        print("\n  MAIN MENU")
        print("  ---------")
        print("    [T] Track today's habits")
        print("    [S] View today's summary")
        print("    [R] Reset all entries (new day)")
        print("    [Q] Quit")

        choice = input("\n  Choice: ").strip().lower()

        if choice == "t":
            # --- TRACK ---
            run_tracker()

        elif choice == "s":
            # --- SUMMARY ---
            # Lets user review progress without going through full tracking flow
            show_summary()

        elif choice == "r":
            # --- RESET ---
            # Ask for confirmation before wiping — destructive action
            print("\n  ⚠  This will clear ALL entries for all habits.")
            confirm = input("  Are you sure? (yes / no): ").strip().lower()

            if confirm in ("yes", "y"):
                clear_all_entries()
            else:
                print("  Reset cancelled.")

        elif choice == "q":
            # --- QUIT ---
            print("\n  Goodbye! Stay healthy. 👋")
            break

        else:
            print("  ⚠  Please enter T, S, R, or Q.")


# --- Entry point ---
if __name__ == "__main__":
    main()