import tkinter as tk
from tkinter import scrolledtext, ttk, Listbox
from collections import Counter
import re

def count_word_frequency(text, exclude_words):
    words = re.findall(r'\w+', text.lower())
    words = [word for word in words if word not in exclude_words]
    return Counter(words)

def display_frequencies():
    text = text_input.get("1.0", tk.END)
    exclude_words = exclude_entry.get().lower().split(',')
    exclude_words = [word.strip() for word in exclude_words]
    word_frequencies = count_word_frequency(text, exclude_words)
    
    # Clear the listbox before adding new items
    word_list.delete(0, tk.END)
    
    for word, freq in word_frequencies.items():
        word_list.insert(tk.END, f"{word}: {freq}")

def on_word_select(event):
    selected_index = word_list.curselection()
    selected_text = word_list.get(selected_index).split(":")[0]
    highlight_word(selected_text)

def highlight_word(word):
    # Clear existing tags
    text_input.tag_remove('highlight', '1.0', tk.END)
    
    if not word:
        return
    
    start_pos = '1.0'
    while True:
        start_pos = text_input.search(word, start_pos, stopindex=tk.END)
        if not start_pos:
            break
        end_pos = f"{start_pos}+{len(word)}c"
        text_input.tag_add('highlight', start_pos, end_pos)
        start_pos = end_pos
    text_input.tag_config('highlight', background='yellow')

# Set up the GUI
root = tk.Tk()
root.title("Word Frequency Counter")
root.geometry("600x600")

text_input_label = ttk.Label(root, text="Enter your text below:")
text_input_label.pack(pady=(10,0))
text_input = scrolledtext.ScrolledText(root, height=10, font=('Helvetica', 12), bg='white', fg='black')
text_input.pack(pady=(0,10))

exclude_label = ttk.Label(root, text="Words to exclude (comma-separated):")
exclude_label.pack()
exclude_entry = ttk.Entry(root)
exclude_entry.pack()

count_button = ttk.Button(root, text="Count Word Frequencies", command=display_frequencies)
count_button.pack(pady=(10,10))

word_list_label = ttk.Label(root, text="Click a word to highlight:")
word_list_label.pack(pady=(10,0))
word_list = Listbox(root, height=10)
word_list.pack(pady=(0,10))
word_list.bind('<<ListboxSelect>>', on_word_select)

root.mainloop()
