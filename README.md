# Welcome to My Python Learning Journey! 🚀

This repository is my personal space for learning the Python programming language, one example at a time. I believe in learning by doing, so each file in this repository represents a new concept or a step forward in my Python journey.

## Core Python Concepts

A key part of writing clean, readable Python code is understanding its fundamental syntax and structure.

### Indentation: The Foundation of Python

Unlike other languages that use brackets (`{}`), Python uses indentation to define code blocks. This is not just for style—it's a syntax rule. Consistent indentation (the standard is 4 spaces) is mandatory.

```python
# This is a code block
if net_savings > daily_saving_goal:
    # This indented block only runs if the condition is true
    print("Excellent! You exceeded your goal.")
    print("Keep up the great work!")

# This line is not indented, so it's outside the if block
print("Summary complete.")
```

### Defining Functions

Functions are reusable blocks of code. In Python, you define them using the `def` keyword. Modern Python encourages using type hints to specify the types of parameters and the return value.

```python
#           Parameter with type hint
#           |
def get_positive_float(prompt: str) -> float | None:
#                              |           |
#                              Return type hint (can be a float or None)

    """
    This is a docstring, explaining what the function does.
    """
    raw = input(prompt)
    if not raw:
        return None # Returns a value of type None
    return float(raw) # Returns a value of type float
```

### Looping and Iteration

Loops are used to repeat a block of code.

*   **`for` loop**: Iterates over a sequence (like a list or dictionary).

```python
# Iterating over the keys and values of a dictionary
for habit_name, config in HABITS.items():
    print(f"Checking habit: {habit_name}")
```

*   **`while` loop**: Repeats as long as a condition is true.

```python
# Looping until the user is done entering values
entry_number = 1
while True:
    value = get_positive_float(f"Entry {entry_number}: ")
    if value is None:
        break # Exit the loop
    entries.append(value)
    entry_number += 1
```

### Comprehensions: A Pythonic Shortcut

Comprehensions provide a concise way to create lists, dictionaries, or sets. They can often replace a `for` loop with a single, more readable line.

*   **Dictionary Comprehension**: Creates a new dictionary from an iterable.

```python
# This line from healthyhabittracker.py...
totals_summary = {name: cfg["total"] for name, cfg in HABITS.items()}

# ...is a compact and efficient way of writing this for loop:
totals_summary = {}
for name, cfg in HABITS.items():
    totals_summary[name] = cfg["total"]
```

### Naming Conventions (PEP 8)

*   **`snake_case`**: For all variable and function names (e.g., `net_savings`, `calculate_total()`).
*   **`UPPERCASE_SNAKE_CASE`**: For constants (e.g., `HABITS`, `TAX_RATE`).
*   **`PascalCase`**: For class names (e.g., `class MyNewClass:`).

## My First Step: A Personal Budget Tracker

The first example, `personalbudgettracker.py`, is a simple command-line tool to track daily income and expenses.

### Concepts Learned:

*   **User Input:** Using the `input()` function to get data from the user.
*   **Data Types:** Using `float()` to convert strings to numbers.
*   **Variables:** Storing data in variables.
*   **Basic Arithmetic:** Performing calculations like subtraction.
*   **Formatted Output:** Using f-strings to display information to the user.
*   **Conditional Logic:** Using `if`, `elif`, and `else` to make decisions based on the user's savings.

### How to Run It:

```bash
python personalbudgettracker.py
```

I'm excited to continue this journey and add more examples as I learn!

## Next Step: A Healthy Habit Tracker

The `healthyhabittracker/healthyhabittracker.py` example is designed to help users track their daily healthy habits.

### Concepts Learned:

*   **Data-Driven Design:** Using a central `HABITS` dictionary to define the application's behavior, making the code more modular and easier to extend.
*   **Functions:** Organizing code into reusable blocks with clear purposes (e.g., `collect_entries`, `evaluate_habit`).
*   **Dictionaries:** Storing complex, related data in a key-value format.
*   **Lists:** Collecting multiple user inputs into a list.
*   **Loops:** Using `for` loops to iterate over dictionaries and `while` loops for repetitive input.
*   **Error Handling:** Using `try...except` to gracefully handle invalid user input without crashing.
*   **Type Hinting:** Adding type annotations (`str`, `float`, `list`, `dict`) to improve code clarity and allow for static analysis.
*   **Main Block:** Using `if __name__ == "__main__":` to create a clear entry point for the script.

### How to Run It:

```bash
python healthyhabittracker/healthyhabittracker.py
```
