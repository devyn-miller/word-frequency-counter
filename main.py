from collections import Counter
import re
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk

def count_word_frequency(text, exclude_words):
    words = re.findall(r'\w+', text.lower())
    # Exclude specified words
    words = [word for word in words if word not in exclude_words]
    word_counts = Counter(words)
    return word_counts

def display_frequencies():
    text = text_input.get("1.0", tk.END)
    exclude_words = exclude_entry.get().lower().split(',')
    exclude_words = [word.strip() for word in exclude_words]
    word_frequencies = count_word_frequency(text, exclude_words)
    
    # Sort based on the user's choice
    sort_by_least = sort_var.get()
    word_frequencies = word_frequencies.most_common()
    if sort_by_least:
        word_frequencies.reverse()
    
    result_text = "\n".join([f"{word}: {frequency}" for word, frequency in word_frequencies])
    result_display.delete("1.0", tk.END)
    result_display.insert(tk.END, result_text)

# Set up the GUI
root = tk.Tk()
root.title("Word Frequency Counter")
root.geometry("400x600")  # Set initial size of the window

style = ttk.Style()
style.configure('TLabel', font=('Arial', 10))
style.configure('TButton', font=('Arial', 10))

# Create a text input area
text_input_label = ttk.Label(root, text="Enter your text below:")
text_input_label.pack(pady=(10,0))
text_input = scrolledtext.ScrolledText(root, height=10)
text_input.pack(pady=(0,10))

# Exclude words entry
exclude_label = ttk.Label(root, text="Words to exclude (comma-separated):")
exclude_label.pack()
exclude_entry = ttk.Entry(root)
exclude_entry.pack()

# Sorting option
sort_var = tk.BooleanVar()
sort_check = ttk.Checkbutton(root, text="Sort by least frequent", variable=sort_var)
sort_check.pack()

# Button to trigger word frequency count
count_button = ttk.Button(root, text="Count Word Frequencies", command=display_frequencies)
count_button.pack(pady=(10,10))

# Area to display the results
result_display = scrolledtext.ScrolledText(root, height=10)
result_display.pack(pady=(0,10))

# Run the application
root.mainloop()
