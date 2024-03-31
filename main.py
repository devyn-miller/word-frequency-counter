from collections import Counter
import re
import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk, simpledialog

def count_word_frequency(text, exclude_words):
    words = re.findall(r'\w+', text.lower())
    words = [word for word in words if word not in exclude_words]
    word_counts = Counter(words)
    return word_counts

def display_frequencies():
    text = text_input.get("1.0", tk.END)
    exclude_words = exclude_entry.get().lower().split(',')
    exclude_words = [word.strip() for word in exclude_words]
    word_frequencies = count_word_frequency(text, exclude_words)
    
    sort_by_least = sort_var.get()
    word_frequencies_list = word_frequencies.most_common()
    if sort_by_least:
        word_frequencies_list.reverse()
    
    total_diff_words = len(word_frequencies)
    word_count = sum(word_frequencies.values())
    char_count_incl_spaces = len(text) - 1  # Subtract 1 to exclude the final newline character
    char_count_excl_spaces = len(text.replace(" ", "").replace("\n", ""))
    
    result_text = f"Total different words: {total_diff_words}\n"
    result_text += f"Total words: {word_count}\n"
    result_text += f"Characters (including spaces): {char_count_incl_spaces}\n"
    result_text += f"Characters (excluding spaces): {char_count_excl_spaces}\n\n"
    for word, frequency in word_frequencies_list:
        result_text += f"{word}: {frequency}\n"
    
    result_display.delete("1.0", tk.END)
    result_display.insert(tk.END, result_text)

def adjust_font_size():
    new_size = simpledialog.askinteger("Font Size", "Enter new font size:", minvalue=8, maxvalue=32)
    if new_size:
        text_input.config(font=('Helvetica', new_size), fg='black')
        result_display.config(font=('Helvetica', new_size), fg='black')

# Set up the GUI
root = tk.Tk()
root.title("Word Frequency Counter")
root.geometry("400x600")

style = ttk.Style()
style.configure('TLabel', font=('Arial', 10))
style.configure('TButton', font=('Arial', 10))

text_input_label = ttk.Label(root, text="Enter your text below:")
text_input_label.pack(pady=(10,0))
text_input = scrolledtext.ScrolledText(root, height=10, font=('Helvetica', 12), bg='white', fg='black')
text_input.pack(pady=(0,10))

exclude_label = ttk.Label(root, text="Words to exclude (comma-separated):")
exclude_label.pack()
exclude_entry = ttk.Entry(root)
exclude_entry.pack()

sort_var = tk.BooleanVar()
sort_check = ttk.Checkbutton(root, text="Sort by least frequent", variable=sort_var)
sort_check.pack()

count_button = ttk.Button(root, text="Count Word Frequencies", command=display_frequencies)
count_button.pack(pady=(10,10))

font_button = ttk.Button(root, text="Adjust Font Size", command=adjust_font_size)
font_button.pack(pady=(5,10))

result_display = scrolledtext.ScrolledText(root, height=10, font=('Helvetica', 12), bg='white', fg='black')
result_display.pack(pady=(0,10))

root.mainloop()
