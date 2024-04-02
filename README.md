---
runme:
  id: 01HTE2M7YAS03VSQDSKHM7PEZ0
  version: v3
---

# word-frequency-counter

# Project Overview

This project is a Word Frequency Counter application built using Python and the Tkinter library for the graphical user interface (GUI). It allows users to input text, specify words to exclude, and then analyze the text to display the frequency of each word. Additionally, users can visualize the frequency of the top words through a bar chart and highlight specific words within the input text.

## Features

- **Text Input**: Users can paste or type text into a multi-line input field.
- **Exclude Words**: Users can specify words to exclude from the frequency analysis. This can include custom words or selecting common words to exclude (e.g., top 50, 100, or 150 common words).
- **Frequency Analysis**: The application counts the frequency of each word in the input text, excluding specified words, and displays the results in a list.
- **Text Statistics**: Displays statistics about the text, including the total number of different words, total word count, and character count (with and without spaces).
- **Word Highlighting**: Users can select words from the frequency list to highlight them in the input text area.
- **Visualization**: Users can plot the frequency of the top N words in a bar chart within the application.
- **Copy to Clipboard**: Allows users to copy the list of words and their frequencies to the clipboard.

## How to Use

1. **Start the Application**: Run `main.py` to start the application.
2. **Input Text**: Enter your text in the "Enter your text below:" field.
3. **Exclude Words (Optional)**: Enter any words you wish to exclude in the "Words to exclude" field. You can also select to exclude common words using the dropdown menu.
4. **Analyze**: Click on "Count Word Frequencies" to analyze the text. The frequencies will be displayed in a list, and text statistics will be shown below.
5. **Highlight Words (Optional)**: Click on a word in the list to highlight it in the input text area. You can select multiple words using Ctrl (Cmd on macOS) or Shift.
6. **Visualize (Optional)**: Click on "Plot Top Word Frequencies" to visualize the frequency of the top N words.
7. **Copy to Clipboard (Optional)**: Click on "Copy to Clipboard" to copy the list of words and their frequencies.

## Dependencies

- Python 3
- Tkinter
- matplotlib
- pyperclip
- ttkthemes (for themed GUI elements)

Ensure you have Python 3 installed along with the necessary libraries before running the application.

## Running the Application

To run the application, navigate to the project directory in your terminal or command prompt and execute:

```python main.py```

This will launch the GUI where you can start interacting with the application.

## Contributing

Contributions to the project are welcome! Please refer to the contributing guidelines for more information on how to contribute.

Thank you for using or contributing to the Word Frequency Counter project!
