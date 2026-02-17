# ============================================================
# Healthy Habits Tracker — Dictionary-driven version
# Adding a new habit = one new entry in HABITS. Nothing else changes.
# ============================================================

# --- Habit configuration dictionary ---
# Each key is the habit name. Each value holds its unit and daily threshold.
# This is your single source of truth — the rest of the code is data-agnostic.
HABITS: dict[str, dict] = {
    "Water Intake": {"unit": "cups",    "threshold": 8},
    "Exercise":     {"unit": "minutes", "threshold": 30},
    "Sleep":        {"unit": "hours",   "threshold": 7},
}


def get_positive_float(prompt: str) -> float | None:
    """
    Prompts for a positive numeric value.
    Returns float if valid, None if user types 'done' or presses Enter.
    Handles invalid input without crashing.
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
            return value
        except ValueError:
            print("  ⚠  Invalid input. Please enter a number (or 'done' to finish).")


def collect_entries(habit_name: str, unit: str) -> list[float]:
    """
    Collects multiple entries for a single habit.
    Returns a list of all entered values.
    """
    entries = []
    print(f"\n--- {habit_name} Tracker ({unit}) ---")
    print("  Enter each entry one at a time. Type 'done' (or press Enter) when finished.")

    entry_number = 1
    while True:
        value = get_positive_float(f"  Entry {entry_number} ({unit}): ")
        if value is None:
            break
        entries.append(value)
        entry_number += 1

    return entries


def evaluate_habit(habit_name: str, total: float, threshold: float, unit: str) -> None:
    """
    Compares total against threshold and prints a pass/fail status message.
    """
    if total >= threshold:
        print(f"  ✅ {habit_name}: {total:.1f} {unit} — Goal met! (Target: {threshold} {unit})")
    else:
        shortfall = threshold - total
        print(f"  ❌ {habit_name}: {total:.1f} {unit} — {shortfall:.1f} {unit} below target (Target: {threshold} {unit})")


def run_tracker() -> None:
    """
    Main orchestration function.

    Flow:
      1. Iterate over HABITS dict to collect entries for each habit.
      2. Compute totals and store back into the dict (single data structure throughout).
      3. Iterate again to evaluate and display results.

    Adding a new habit requires zero changes here — only update HABITS above.
    """
    print("=" * 50)
    print("       🌿 Healthy Habits Tracker 🌿")
    print("=" * 50)

    # --- DEBUG: Confirm habits loaded from config ---
    print(f"[DEBUG] Habits loaded: {list(HABITS.keys())}")

    # --- Step 1 & 2: Collect entries and compute totals ---
    # We iterate over the dict once, collect user input, and store the total
    # back into the same dict under a new "total" key.
    for habit_name, config in HABITS.items():
        entries = collect_entries(habit_name, config["unit"])
        config["total"] = sum(entries)   # sum([]) == 0.0, so empty input is safe

    # --- DEBUG: Confirm all totals before evaluation ---
    totals_summary = {name: cfg["total"] for name, cfg in HABITS.items()}
    print(f"\n[DEBUG] Computed totals: {totals_summary}")

    # --- Step 3: Evaluate and display summary ---
    print("\n" + "=" * 50)
    print("           📊 Daily Summary")
    print("=" * 50)

    for habit_name, config in HABITS.items():
        evaluate_habit(habit_name, config["total"], config["threshold"], config["unit"])

    print("=" * 50)
    print("  Keep it up! Small habits compound over time. 💪")
    print("=" * 50)


# --- Entry point ---
if __name__ == "__main__":
    run_tracker()