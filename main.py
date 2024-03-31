import tkinter as tk
from tkinter import scrolledtext, ttk, Listbox, simpledialog, StringVar, messagebox, colorchooser
from collections import Counter
import re
import pyperclip
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Define the common words
top_50_words = set("the, of, and, a, to, in, is, you, that, it, he, for, was, on, are, as, not, but, what, all, were, when, we, there, can, an, your, which, their, said, if, do, into, has, more, her, two, like, him, see, time, could, no, make, than, first, been, its, water, long".split(", "))
top_100_words = top_50_words.union("little, very, after, words, called, just, where, most, know, get, through, back, much, before, think, also, around, another, came, come, work, three, word, must, because, does, part, even, place, well, with, his, they, at, be, this, from, I, have, or, by, one, had, will, each, about, how, up, out, them".split(", "))
top_150_words = top_100_words.union("then, she, many, some, so, these, would, who, now, people, my, made, over, did, down, only, way, find, use, may, other, go, good, new, write, our, used, me, man, too, any, day, same, right, look, such, here, take, why, things, help, put, years, different, away, again, off, went, old, number".split(", "))

def count_word_frequency(text, exclude_words):
    words = re.findall(r'\w+', text.lower())
    words = [word for word in words if word not in exclude_words]
    return Counter(words)

def display_frequencies():
    text = text_input.get("1.0", tk.END)
    exclude_words_input = exclude_entry.get().lower().split(',')
    exclude_words = set(word.strip() for word in exclude_words_input)
    
    # Append common words based on user selection
    common_words_selection = common_words_var.get()
    if common_words_selection == "Top 50":
        exclude_words.update(top_50_words)
    elif common_words_selection == "Top 100":
        exclude_words.update(top_100_words)
    elif common_words_selection == "Top 150":
        exclude_words.update(top_150_words)
    
    word_frequencies = count_word_frequency(text, exclude_words)
    
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
    selected_indices = word_list.curselection()
    selected_color = highlight_color_var.get()  # Get the selected color
    
    # Clear existing highlights
    for tag in text_input.tag_names():
        text_input.tag_delete(tag)
    
    for index in selected_indices:
        try:
            selected_text = word_list.get(index)
            word = selected_text.split(":")[0]
            highlight_word(word, selected_color)
        except tk.TclError as e:
            print(f"Error accessing Listbox item: {e}")

def highlight_word(word, color):
    start_pos = '1.0'
    while True:
        start_pos = text_input.search(word, start_pos, stopindex=tk.END)
        if not start_pos:
            break
        end_pos = f"{start_pos}+{len(word)}c"
        tag_name = f"highlight_{word}"
        text_input.tag_add(tag_name, start_pos, end_pos)
        text_input.tag_config(tag_name, background=color)
        start_pos = end_pos

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

def copy_to_clipboard():
    text_to_copy = ""
    for item in word_list.get(0, tk.END):
        text_to_copy += item + "\n"
    pyperclip.copy(text_to_copy)
    messagebox.showinfo("Copied", "Words and frequencies copied to clipboard!")

# Set up the GUI
root = tk.Tk()
root.title("Word Frequency Counter")
root.geometry("800x900")  # Adjusted to accommodate the new stats area and plotting area

text_input_label = ttk.Label(root, text="Enter your text below:")
text_input_label.pack(pady=(10,0))
text_input = scrolledtext.ScrolledText(root, height=10, font=('Helvetica', 12), bg='white', fg='black')
text_input.pack(pady=(0,10))

# Set focus to the text_input widget to show the blinking cursor
text_input.focus_set()

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
word_list = Listbox(root, height=10, selectmode=tk.MULTIPLE)
word_list.pack(pady=(0,10))
word_list.bind('<<ListboxSelect>>', on_word_select)

# New stats display area
stats_display_label = ttk.Label(root, text="Text Statistics:")
stats_display_label.pack(pady=(10,0))
stats_display = scrolledtext.ScrolledText(root, height=5, font=('Helvetica', 10), bg='white', fg='black')
stats_display.pack(pady=(0,10))

# Dropdown for common words selection
common_words_var = StringVar()
common_words_var.set("None")  # default value
common_words_label = ttk.Label(root, text="Exclude common words:")
common_words_label.pack()
common_words_dropdown = ttk.OptionMenu(root, common_words_var, "None", "Top 50", "Top 100", "Top 150")
common_words_dropdown.pack()

# Copy to Clipboard button
copy_button = ttk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard)
copy_button.pack(pady=(5,10))

root.mainloop()
