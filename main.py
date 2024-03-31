from collections import Counter
import re
import tkinter as tk
from tkinter import scrolledtext
from tkinter import messagebox

def count_word_frequency(text):
    words = re.findall(r'\w+', text.lower())
    word_counts = Counter(words)
    return word_counts.most_common()

def display_frequencies():
    text = text_input.get("1.0", tk.END)
    word_frequencies = count_word_frequency(text)
    result_text = "\n".join([f"{word}: {frequency}" for word, frequency in word_frequencies])
    result_display.delete("1.0", tk.END)
    result_display.insert(tk.END, result_text)

# Set up the GUI
root = tk.Tk()
root.title("Word Frequency Counter")

# Create a text input area
text_input_label = tk.Label(root, text="Enter your text below:")
text_input_label.pack()
text_input = scrolledtext.ScrolledText(root, height=10)
text_input.pack()

# Button to trigger word frequency count
count_button = tk.Button(root, text="Count Word Frequencies", command=display_frequencies)
count_button.pack()

# Area to display the results
result_display = scrolledtext.ScrolledText(root, height=10)
result_display.pack()

# Run the application
root.mainloop()
