import tkinter as tk
from tkinter import scrolledtext
import hashlib
import random
import string
# ==========================
# PASSWORD STRENGTH
# ==========================
def calculate_strength(password):
    score = 0
    if len(password) >= 8:
        score += 2
    if any(ch.isupper() for ch in password):
        score += 1
    if any(ch.islower() for ch in password):
        score += 1
    if any(ch.isdigit() for ch in password):
        score += 1
    if any(not ch.isalnum() for ch in password):
        score += 1
    return score
# ==========================
# PATTERN DETECTION
# ==========================
def detect_patterns(password):
    issues = []
    weak_passwords = {
        "password",
        "admin",
        "qwerty",
        "welcome",
        "123456"
    }

    if password.lower() in weak_passwords:
        issues.append("Common password detected")

    sequences = [
        "1234",
        "2345",
        "3456",
        "4567",
        "5678",
        "6789"
    ]

    for seq in sequences:
        if seq in password:
            issues.append("Sequential numbers found")
            break

    for i in range(len(password) - 2):
        if password[i] == password[i+1] == password[i+2]:
            issues.append("Repeated characters found")
            break

    return issues


# ==========================
# HASHING
# ==========================
def generate_hash(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ==========================
# CRACK TIME ESTIMATION
# ==========================
def estimate_crack_time(password):

    charset_size = 0

    if any(ch.islower() for ch in password):
        charset_size += 26

    if any(ch.isupper() for ch in password):
        charset_size += 26

    if any(ch.isdigit() for ch in password):
        charset_size += 10

    if any(not ch.isalnum() for ch in password):
        charset_size += 32

    if charset_size == 0:
        return "Unknown"

    combinations = charset_size ** len(password)

    guesses_per_second = 1_000_000_000

    seconds = combinations / guesses_per_second

    if seconds < 60:
        return "Less than 1 minute"

    elif seconds < 3600:
        return f"{int(seconds//60)} minutes"

    elif seconds < 86400:
        return f"{int(seconds//3600)} hours"

    elif seconds < 31536000:
        return f"{int(seconds//86400)} days"

    else:
        return f"{int(seconds//31536000)} years"


# ==========================
# SUGGESTIONS
# ==========================
def generate_suggestions(password, issues):

    suggestions = []

    if len(password) < 8:
        suggestions.append("Increase password length")

    if not any(ch.isupper() for ch in password):
        suggestions.append("Add uppercase letters")

    if not any(ch.islower() for ch in password):
        suggestions.append("Add lowercase letters")

    if not any(ch.isdigit() for ch in password):
        suggestions.append("Add numbers")

    if not any(not ch.isalnum() for ch in password):
        suggestions.append("Add special characters")

    if "Repeated characters found" in issues:
        suggestions.append("Avoid repeated characters")

    if "Sequential numbers found" in issues:
        suggestions.append("Avoid sequential numbers")

    if "Common password detected" in issues:
        suggestions.append("Avoid common passwords")

    return suggestions
# ==========================
# SHOW / HIDE PASSWORD
# ==========================
def toggle_password():

    if show_password.get():
        password_entry.config(show="")

    else:
        password_entry.config(show="*")
# ==========================
# PASSWORD GENERATOR
# ==========================
def generate_password():

    chars = (
        string.ascii_letters +
        string.digits +
        string.punctuation
    )

    password = ''.join(
        random.choice(chars)
        for _ in range(12)
    )

    password_entry.delete(0, tk.END)
    password_entry.insert(0, password)


# ==========================
# CLEAR
# ==========================
def clear_fields():

    password_entry.delete(0, tk.END)

    result_text.delete("1.0", tk.END)

    strength_bar.delete("all")


# ==========================
# ANALYZE
# ==========================
def analyze_password():

    password = password_entry.get()

    if password == "":
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Please enter a password.")
        return

    score = calculate_strength(password)

    if score <= 2:
        strength = "WEAK"
        color = "red"

    elif score <= 4:
        strength = "MEDIUM"
        color = "orange"

    else:
        strength = "STRONG"
        color = "green"

    issues = detect_patterns(password)

    hash_value = generate_hash(password)

    crack_time = estimate_crack_time(password)

    suggestions = generate_suggestions(password, issues)

    strength_bar.delete("all")

    width = (score / 6) * 300

    strength_bar.create_rectangle(
        0,
        0,
        width,
        25,
        fill=color
    )

    result = ""

    result += "PASSWORD ANALYSIS REPORT\n"
    result += "=" * 50 + "\n\n"

    result += f"Strength Score : {score}/6\n"
    result += f"Password Strength : {strength}\n\n"

    result += "Detected Issues:\n"

    if issues:
        for issue in issues:
            result += f"• {issue}\n"
    else:
        result += "• No Weak Patterns Found\n"
    result += "\n"
    result += "SHA-256 Hash:\n"
    result += hash_value + "\n\n"
    result += "Estimated Crack Time:\n"
    result += crack_time + "\n\n"
    result += "Suggestions:\n"
    if suggestions:
        for suggestion in suggestions:
            result += f"✓ {suggestion}\n"
    else:
        result += "✓ Excellent Password!\n"
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END,result)
# ==========================
# GUI
# ==========================
root = tk.Tk()

root.title("Secure Password Analyzer")
root.geometry("850x750")
root.configure(bg="#1E1E1E")

# Title
title_label = tk.Label(
    root,
    text="🔐 Secure Password Analyzer",
    font=("Segoe UI", 22, "bold"),
    fg="white",
    bg="#1E1E1E"
)

title_label.pack(pady=20)

# Password Label
password_label = tk.Label(
    root,
    text="Enter Password",
    font=("Segoe UI", 12),
    fg="white",
    bg="#1E1E1E"
)

password_label.pack()

# Password Entry
password_entry = tk.Entry(
    root,
    width=35,
    show="*",
    font=("Consolas", 14),
    bd=3
)

password_entry.pack(pady=10)

# Show Password
show_password = tk.BooleanVar()

show_checkbox = tk.Checkbutton(
    root,
    text="Show Password",
    variable=show_password,
    command=toggle_password,
    fg="white",
    bg="#1E1E1E",
    selectcolor="#1E1E1E"
)

show_checkbox.pack()

# Strength Meter
strength_label = tk.Label(
    root,
    text="Strength Meter",
    fg="white",
    bg="#1E1E1E",
    font=("Segoe UI", 10)
)

strength_label.pack(pady=5)

strength_bar = tk.Canvas(
    root,
    width=300,
    height=25,
    bg="white"
)

strength_bar.pack(pady=10)

# Buttons
analyze_button = tk.Button(
    root,
    text="Analyze Password",
    command=analyze_password,
    bg="#007ACC",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    width=25
)

analyze_button.pack(pady=5)

generate_button = tk.Button(
    root,
    text="Generate Strong Password",
    command=generate_password,
    bg="#28A745",
    fg="white",
    font=("Segoe UI", 11, "bold"),
    width=25
)

generate_button.pack(pady=5)

clear_button = tk.Button(
    root,
    text="Clear",
    command=clear_fields,
    bg="#444444",
    fg="white",
    font=("Segoe UI", 11),
    width=25
)

clear_button.pack(pady=5)

# Results Area
result_text = scrolledtext.ScrolledText(
    root,
    width=90,
    height=22,
    font=("Consolas", 10),
    bg="#252526",
    fg="white"
)

result_text.pack(pady=20)

# Footer
footer = tk.Label(
    root,
    text="DSA Project - Secure Password Analyzer with Attack Simulation",
    fg="gray",
    bg="#1E1E1E",
    font=("Segoe UI", 10)
)

footer.pack(side="bottom", pady=10)

root.mainloop()