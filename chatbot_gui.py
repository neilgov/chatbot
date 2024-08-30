import tkinter as tk
import json
from difflib import get_close_matches

# Load questions and answers from the JSON file
def load_qa_data(filename):
    with open(filename, "r", encoding="utf-8") as file:
        return json.load(file)

# Function to find the best matching question within a category and return the corresponding answer
def get_answer(category, question, qa_data):
    if category in qa_data:
        questions = list(qa_data[category].keys())
        closest_match = get_close_matches(question, questions, n=1, cutoff=0.5)
        if closest_match:
            return qa_data[category][closest_match[0]]
        else:
            return "I don't have an answer for that in the selected category."
    else:
        return "Category not found. Please choose a valid category."

# Function to handle user input and display the answer
def ask_question():
    category = category_var.get()
    question = question_var.get()
    answer = get_answer(category, question, qa_data)
    text_area.insert(tk.END, "You: " + question + "\n")
    text_area.insert(tk.END, "Bot: " + answer + "\n")
    text_area.see(tk.END)

# Function to update the question dropdown based on the selected category
def update_questions(*args):
    category = category_var.get()
    question_menu['menu'].delete(0, 'end')

    if category in qa_data:
        questions = qa_data[category]
        for question in questions.keys():
            question_menu['menu'].add_command(label=question, command=tk._setit(question_var, question))
    question_var.set('Select a question')

# Load the question and answer data
qa_data = load_qa_data("qa_data.json")

# Set up the GUI
root = tk.Tk()
root.title("Chatbot")

category_var = tk.StringVar(root)
question_var = tk.StringVar(root)

category_label = tk.Label(root, text="Category:")
category_label.pack()

category_menu = tk.OptionMenu(root, category_var, *qa_data.keys())
category_menu.pack()

question_label = tk.Label(root, text="Questions:")
question_label.pack()

question_menu = tk.OptionMenu(root, question_var, '')
question_menu.pack()

category_var.trace('w', update_questions)

# Configure the text area
text_area = tk.Text(root, height=20, width=80, wrap=tk.WORD, font=("Arial", 12), bg="white", fg="black")
text_area.pack()

ask_button = tk.Button(root, text="Ask", command=ask_question)
ask_button.pack()

root.mainloop()
