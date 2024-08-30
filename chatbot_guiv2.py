import tkinter as tk
from tkinter import simpledialog, messagebox
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
    category = category_entry.get()
    question = entry.get()
    answer = get_answer(category, question, qa_data)
    text_area.insert(tk.END, "You: " + question + "\n")
    text_area.insert(tk.END, "Bot: " + answer + "\n")
    entry.delete(0, tk.END)

# Function to add a new question and answer to the JSON data
def add_question():
    category = simpledialog.askstring("Input", "Enter the category:")
    if not category:
        return
    
    question = simpledialog.askstring("Input", "Enter the question:")
    if not question:
        return
    
    answer = simpledialog.askstring("Input", "Enter the answer:")
    if not answer:
        return
    
    if category not in qa_data:
        qa_data[category] = {}
    
    qa_data[category][question] = answer
    
    with open("qa_data.json", "w", encoding="utf-8") as file:
        json.dump(qa_data, file, indent=4)
    
    messagebox.showinfo("Success", "Question added successfully!")

# Load the question and answer data
qa_data = load_qa_data("qa_data.json")

# Set up the GUI
root = tk.Tk()
root.title("Chatbot")

category_label = tk.Label(root, text="Category:")
category_label.pack()

category_entry = tk.Entry(root, width=50)
category_entry.pack()

text_area = tk.Text(root, height=20, width=50)
text_area.pack()

entry = tk.Entry(root, width=50)
entry.pack()

ask_button = tk.Button(root, text="Ask", command=ask_question)
ask_button.pack()

add_question_button = tk.Button(root, text="Add Question", command=add_question)
add_question_button.pack()

root.mainloop()
