# Welcome to My Python Learning Journey! 🚀

This repository is my personal space for learning the Python programming language, one example at a time. I believe in learning by doing, so each file in this repository represents a new concept or a step forward in my Python journey.

## Core Coding Conventions

A key part of writing clean, readable Python code is adhering to the **PEP 8** style guide.

### Naming Conventions:

*   **`snake_case`**: For all variable and function names. This is the standard for making code easy to read (e.g., `net_savings`, `calculate_total()`).
*   **`UPPERCASE_SNAKE_CASE`**: For constants, which are variables whose values are not intended to change (e.g., `HABITS`, `TAX_RATE`).
*   **`PascalCase`**: For class names (e.g., `class MyNewClass:`). We haven't used classes yet, but it's good to know!

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
