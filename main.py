import tkinter as tk
from tkinter import scrolledtext, ttk, Listbox, simpledialog, StringVar, messagebox, colorchooser
from collections import Counter
import re
import pyperclip
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from ttkthemes import ThemedTk

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
    exclude_words_input = exclude_text.get("1.0", "end-1c").lower().split(',')
    exclude_words = set(word.strip() for word in exclude_words_input)
    
    # Append common words based on user selection
    common_words_selection = common_words_var.get()
    if common_words_selection == "Top 50":
        exclude_words.update(top_50_words)
    elif common_words_selection == "Top 100":
        exclude_words.update(top_100_words)
    elif common_words_selection == "Top 150":
        exclude_words.update(top_150_words)
    
    # Update the exclude_text widget with the new exclude words
    exclude_text.delete("1.0", tk.END)
    exclude_text.insert("1.0", ', '.join(exclude_words))
    
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
    if not selected_indices:
        print("No item selected or invalid selection")
        return  # Exit the function if no selection is made

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
    exclude_words = exclude_text.get("1.0", "end-1c").lower().split(',')
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
root = ThemedTk(theme="equilux")
root.title("Word Frequency Counter")
root.geometry("800x900")  # Adjusted to accommodate the new stats area and plotting area

# Use a modern and consistent font
modern_font = ('Arial', 12, 'bold')  # Making the font bold for better readability

# Use a higher contrast color scheme
bg_color = '#ffffff'  # White background for higher contrast
text_color = '#000000'  # Black text for better readability
button_color = '#f2f2f2'  # Light grey for buttons
highlight_color = '#cce7ff'  # Light blue highlight color

root.configure(bg=bg_color)  # Set the background color for the root window

# Welcome message box
def show_welcome_message():
    messagebox.showinfo("Welcome", "Welcome to the Word Frequency Counter!\n\n"
                                    "1. Enter your text in the provided text area.\n"
                                    "2. Optionally, specify words to exclude.\n"
                                    "3. Use the 'Count Word Frequencies' button to see the frequencies of each word.\n"
                                    "4. Highlight words by clicking on them in the list.\n"
                                    "5. Use the 'Plot Top Word Frequencies' to visualize the data.\n"
                                    "6. 'Copy to Clipboard' allows you to copy the list of words and their frequencies.\n\n"
                                    "Enjoy analyzing your text!")

# Call the welcome message function after the main window is set up
root.after(100, show_welcome_message)

# Apply the modern font and higher contrast color scheme to labels
text_input_label = ttk.Label(root, text="Enter your text below (Paste your text here to analyze word frequencies):", font=modern_font, background=bg_color, foreground=text_color)
text_input_label.pack(pady=(10,0))

# Apply the modern font and color scheme to the text input
text_input = scrolledtext.ScrolledText(root, height=10, font=('Helvetica', 12), bg='white', fg=text_color)
text_input.pack(pady=(0,10), padx=10)

# Set focus to the text_input widget to show the blinking cursor
text_input.focus_set()

exclude_label = ttk.Label(root, text="Words to exclude (comma-separated, e.g., 'and, the, a'):", font=modern_font, background=bg_color, foreground=text_color)
exclude_label.pack()
# Create a Text widget for words to exclude
exclude_text = tk.Text(root, height=1, width=40, wrap="none", font=modern_font)  # Set wrap to "none" for horizontal scrolling
exclude_text.pack()

# Create a horizontal scrollbar and attach it to the exclude_text widget
hscroll = tk.Scrollbar(root, orient="horizontal", command=exclude_text.xview)
hscroll.pack(fill="x")
exclude_text.config(xscrollcommand=hscroll.set)

sort_var = tk.BooleanVar()
sort_check = ttk.Checkbutton(root, text="Sort by least frequent", variable=sort_var, style='TCheckbutton')
sort_check.pack()

count_button = ttk.Button(root, text="Count Word Frequencies", command=display_frequencies, style='TButton')
count_button.pack(pady=(10,0), padx=10)

plot_button = ttk.Button(root, text="Plot Top Word Frequencies", command=plot_frequencies, style='TButton')
plot_button.pack(pady=(5,10), padx=10)

word_list_label = ttk.Label(root, text="Click a word to highlight:", font=modern_font, background=bg_color, foreground=text_color)
word_list_label.pack(pady=(10,0))
word_list = Listbox(root, height=10, selectmode=tk.MULTIPLE, bg='white', fg=text_color)
word_list.pack(pady=(0,10), padx=10)
word_list.bind('<<ListboxSelect>>', on_word_select)

# New stats display area
stats_display_label = ttk.Label(root, text="Text Statistics:", font=modern_font, background=bg_color, foreground=text_color)
stats_display_label.pack(pady=(10,0))
stats_display = scrolledtext.ScrolledText(root, height=5, font=('Helvetica', 10), bg='white', fg='black')
stats_display.pack(pady=(0,10), padx=10)

# Dropdown for common words selection
common_words_var = StringVar()
common_words_var.set("None")  # default value
common_words_label = ttk.Label(root, text="Exclude common words: Select a preset list of common words to exclude from the analysis.", font=modern_font, background=bg_color, foreground=text_color)
common_words_label.pack()
# Ensure the update_exclude_words_list function is defined before using it as a command
def update_exclude_words_list(selection):
    print(f"Excluding: {selection}")  # Placeholder function body
common_words_dropdown = ttk.OptionMenu(root, common_words_var, "None", "Top 50", "Top 100", "Top 150", command=update_exclude_words_list)
common_words_dropdown.pack()

# Define available highlight colors
highlight_colors = ["yellow", "light green", "light blue", "pink", "orange"]
highlight_color_var = StringVar()
highlight_color_var.set(highlight_colors[0])  # default to the first color

highlight_color_label = ttk.Label(root, text="Select highlight color:", font=modern_font, background=bg_color, foreground=text_color)
highlight_color_label.pack()
highlight_color_dropdown = ttk.OptionMenu(root, highlight_color_var, *highlight_colors)
highlight_color_dropdown.pack()

# Copy to Clipboard button
copy_button = ttk.Button(root, text="Copy to Clipboard", command=copy_to_clipboard, style='TButton')
copy_button.pack(pady=(5,10), padx=10)

# Customize ttk widgets using a style
style = ttk.Style()
style.configure('TButton', font=modern_font, background=button_color, relief='flat')
style.configure('TLabel', font=modern_font, background=bg_color, foreground=text_color)
style.configure('TCheckbutton', font=modern_font, background=bg_color, foreground=text_color)
style.map('TCheckbutton', background=[('active', highlight_color)])

root.mainloop()
