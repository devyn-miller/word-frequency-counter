import tkinter as tk
from tkinter import scrolledtext, ttk, Listbox, simpledialog
from collections import Counter
import re
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def count_word_frequency(text, exclude_words):
    words = re.findall(r'\w+', text.lower())
    words = [word for word in words if word not in exclude_words]
    return Counter(words)

def display_frequencies():
    text = text_input.get("1.0", tk.END)
    exclude_words = exclude_entry.get().lower().split(',')
    exclude_words = [word.strip() for word in exclude_words]
    word_frequencies = count_word_frequency(text, exclude_words)
    
    # Clear the listbox and stats display before adding new items
    word_list.delete(0, tk.END)
    stats_display.delete("1.0", tk.END)
    
    for word, freq in word_frequencies.items():
        word_list.insert(tk.END, f"{word}: {freq}")
    
    total_diff_words = len(word_frequencies)
    word_count = sum(word_frequencies.values())
    char_count_incl_spaces = len(text) - 1  # Subtract 1 to exclude the final newline character
    char_count_excl_spaces = len(text.replace(" ", "").replace("\n", ""))
    
    stats_text = f"Total different words: {total_diff_words}\n"
    stats_text += f"Total words: {word_count}\n"
    stats_text += f"Characters (including spaces): {char_count_incl_spaces}\n"
    stats_text += f"Characters (excluding spaces): {char_count_excl_spaces}\n"
    
    stats_display.insert(tk.END, stats_text)

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

def plot_frequencies():
    x = simpledialog.askinteger("Input", "How many top words to display?", minvalue=1, maxvalue=100)
    if x is None:
        return  # User cancelled or entered an invalid number
    
    text = text_input.get("1.0", tk.END)
    exclude_words = exclude_entry.get().lower().split(',')
    exclude_words = [word.strip() for word in exclude_words]
    word_frequencies = count_word_frequency(text, exclude_words)
    
    sort_by_least = sort_var.get()
    word_frequencies_list = word_frequencies.most_common()
    if sort_by_least:
        word_frequencies_list = word_frequencies_list[-x:]
    else:
        word_frequencies_list = word_frequencies_list[:x]
    
    words, frequencies = zip(*word_frequencies_list)
    
    # Plotting
    fig, ax = plt.subplots()
    ax.bar(words, frequencies)
    ax.set_xlabel('Words')
    ax.set_ylabel('Frequency')
    ax.set_title('Top Words Frequency')
    
    # Displaying the plot in the tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)  # A tk.DrawingArea.
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)
    canvas.draw()

# Set up the GUI
root = tk.Tk()
root.title("Word Frequency Counter")
root.geometry("800x900")  # Adjusted to accommodate the new stats area and plotting area

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
count_button.pack(pady=(10,0))

plot_button = ttk.Button(root, text="Plot Top Word Frequencies", command=plot_frequencies)
plot_button.pack(pady=(5,10))

word_list_label = ttk.Label(root, text="Click a word to highlight:")
word_list_label.pack(pady=(10,0))
word_list = Listbox(root, height=10)
word_list.pack(pady=(0,10))
word_list.bind('<<ListboxSelect>>', on_word_select)

# New stats display area
stats_display_label = ttk.Label(root, text="Text Statistics:")
stats_display_label.pack(pady=(10,0))
stats_display = scrolledtext.ScrolledText(root, height=5, font=('Helvetica', 10), bg='white', fg='black')
stats_display.pack(pady=(0,10))

root.mainloop()
