import random
import string
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Literal

# === Constants ===
NUMBERS = string.digits
SYMBOLS = string.punctuation
UPPERCASE_LETTERS = string.ascii_uppercase
LOWERCASE_LETTERS = string.ascii_lowercase
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128
WIDGET_ANCHOR: Literal["nw", "n", "ne", "w", "center", "e", "sw", "s", "se"] = "w"

# UI Labels and Messages
GUI_TITLE = "Password Generator"
GUI_DIMENSIONS = "320x360"
GUI_PADDING = {"padx": 5, "pady": 5}
SUCCESS_MESSAGE_COPY = "Password copied to clipboard."
ERROR_MESSAGE_NO_PASSWORD = "Generate a password first to copy it to the clipboard."
ERROR_MESSAGE_INVALID_LENGTH = "The password length must be a positive number."
ERROR_MESSAGE_TOO_LARGE = f"The password length must be at most {MAX_PASSWORD_LENGTH} characters."
ERROR_MESSAGE_MIN_LENGTH = f"The password must be at least {MIN_PASSWORD_LENGTH} characters long."
ERROR_MESSAGE_NO_CHARSETS = "Please select at least one character set."
ERROR_MESSAGE_GROUP_MISMATCH = (
    "Password length must be at least as many as the selected character groups."
)


# === Helper Functions ===
def show_error_message(title, message):
    """Displays an error message using `messagebox.showerror`."""
    messagebox.showerror(title, message)


def get_active_character_sets():
    """Returns active character sets based on selected checkboxes."""
    preferences = {
        "include_numbers": include_numbers.get(),
        "include_symbols": include_symbols.get(),
        "include_uppercase_letters": include_uppercase_letters.get(),
        "include_lowercase_letters": include_lowercase_letters.get(),
    }

    character_sets = {
        "include_numbers": NUMBERS,
        "include_symbols": SYMBOLS,
        "include_uppercase_letters": UPPERCASE_LETTERS,
        "include_lowercase_letters": LOWERCASE_LETTERS,
    }

    # Return character sets where the associated checkbox is checked
    return [character_sets[key] for key, value in preferences.items() if value]


def get_min_password_length():
    """Calculates the minimum password length based on active character sets."""
    selected = [
        include_numbers.get(),
        include_symbols.get(),
        include_uppercase_letters.get(),
        include_lowercase_letters.get(),
    ]
    return max(MIN_PASSWORD_LENGTH, sum(map(bool, selected)))


def is_password_length_valid(length_input, min_length):
    """
    Validates the user-provided password length.

    Args:
        length_input (str): The password length input.
        min_length (int): The minimum allowable password length.
    Returns:
        bool: True if the length is valid, else False (and shows an error message).
    """
    if not (length_input.isdigit() and int(length_input) > 0):
        show_error_message("Error", ERROR_MESSAGE_INVALID_LENGTH)
        return False
    length_int = int(length_input)
    if length_int < min_length:
        show_error_message("Error", ERROR_MESSAGE_MIN_LENGTH)
        return False
    if length_int > MAX_PASSWORD_LENGTH:
        show_error_message("Error", ERROR_MESSAGE_TOO_LARGE)
        return False
    return True


def generate_password_with_charsets(selected_sets, length):
    """
    Generates a password using the selected character sets.

    Args:
        selected_sets (list): Active character sets for the password.
        length (int): Desired total password length.
    Returns:
        str: Generated password.
    """
    required_chars = [random.choice(charset) for charset in selected_sets]
    all_chars = "".join(selected_sets)
    remaining_chars = random.choices(all_chars, k=length - len(required_chars))
    password = required_chars + remaining_chars
    random.shuffle(password)
    return "".join(password)


# === Main Logic ===
def generate_password(event=None):
    """Handles password generation and updates the UI with the generated password."""
    length_input = password_length.get().strip()
    if not length_input:
        show_error_message("Error", "Please provide a valid password length.")
        return
    min_length = get_min_password_length()

    if not is_password_length_valid(length_input, min_length):
        return

    selected_sets = get_active_character_sets()
    if not selected_sets:
        show_error_message("Error", ERROR_MESSAGE_NO_CHARSETS)
        return

    password_length_val = int(length_input)
    if password_length_val < len(selected_sets):
        show_error_message("Error", ERROR_MESSAGE_GROUP_MISMATCH)
        return

    generated_password.set(generate_password_with_charsets(selected_sets, password_length_val))


def copy_to_clipboard():
    """Copies the generated password to the clipboard."""
    password = generated_password.get()
    if password:
        try:
            root.clipboard_clear()
            root.clipboard_append(password)
            root.update()
            messagebox.showinfo("Success", SUCCESS_MESSAGE_COPY)
        except Exception as e:
            show_error_message("Clipboard Error", f"Failed to copy password to clipboard. Error: {str(e)}")
    else:
        show_error_message("Error", ERROR_MESSAGE_NO_PASSWORD)


def update_generate_button_state(*args):
    """Enables or disables the Generate button based on character set selection."""
    active_charsets = get_active_character_sets()
    generate_button.state(["!disabled"] if active_charsets else ["disabled"])


# === GUI Setup ===
def initialize_gui():
    """Sets up the GUI layout."""
    ttk.Label(root, text="How many characters should the password be?").pack(pady=10)
    ttk.Entry(root, textvariable=password_length).pack(**GUI_PADDING)

    # Checkbuttons
    ttk.Checkbutton(root, text="Include Numbers?", variable=include_numbers).pack(
        anchor=WIDGET_ANCHOR, **GUI_PADDING
    )
    ttk.Checkbutton(root, text="Include Symbols?", variable=include_symbols).pack(
        anchor=WIDGET_ANCHOR, **GUI_PADDING
    )
    ttk.Checkbutton(root, text="Include Uppercase Letters?", variable=include_uppercase_letters).pack(
        anchor=WIDGET_ANCHOR, **GUI_PADDING
    )
    ttk.Checkbutton(root, text="Include Lowercase Letters?", variable=include_lowercase_letters).pack(
        anchor=WIDGET_ANCHOR, **GUI_PADDING
    )

    # Buttons and Entries
    global generate_button
    generate_button = ttk.Button(root, text="Generate Password", command=generate_password)
    generate_button.pack(pady=10)

    ttk.Entry(root, textvariable=generated_password, state="readonly", width=35).pack(**GUI_PADDING)
    ttk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard).pack(pady=10)

    # Bind Events
    root.bind("<Return>", generate_password)
    password_length.trace_add("write", update_generate_button_state)
    include_numbers.trace_add("write", update_generate_button_state)
    include_symbols.trace_add("write", update_generate_button_state)
    include_uppercase_letters.trace_add("write", update_generate_button_state)
    include_lowercase_letters.trace_add("write", update_generate_button_state)
    update_generate_button_state()


# === Application Launch ===
root = tk.Tk()
root.title(GUI_TITLE)
root.geometry(GUI_DIMENSIONS)
root.resizable(False, False)

# Variables
password_length = tk.StringVar()
include_numbers = tk.BooleanVar(value=True)
include_symbols = tk.BooleanVar(value=False)
include_uppercase_letters = tk.BooleanVar(value=True)
include_lowercase_letters = tk.BooleanVar(value=True)
generated_password = tk.StringVar()

initialize_gui()
root.mainloop()
