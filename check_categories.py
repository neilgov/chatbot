import tkinter as tk
import json

# Load questions and answers from the JSON file
def load_qa_data(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading JSON data: {e}")
        return {}

# Save questions and answers back to the JSON file
def save_qa_data(filename, data):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)
    except Exception as e:
        print(f"Error saving JSON data: {e}")

# Function to update the category dropdown
def update_categories():
    categories = list(qa_data.keys())
    category_menu["menu"].delete(0, "end")
    for category in categories:
        category_menu["menu"].add_command(label=category, command=tk._setit(category_var, category))

# Function to add a new question
def add_question():
    category = category_var.get()
    question = question_entry.get().strip()
    answer = answer_entry.get().strip()
    
    if category and question and answer:
        if category in qa_data:
            if isinstance(qa_data[category], list):
                qa_data[category].append({"question": question, "answer": answer})
            else:
                qa_data[category] = [{"question": question, "answer": answer}]
        else:
            qa_data[category] = [{"question": question, "answer": answer}]
        
        save_qa_data("new.json", qa_data)
        question_entry.delete(0, tk.END)
        answer_entry.delete(0, tk.END)
        status_var.set(f"Added question to {category}")
        update_categories()  # Ensure categories are updated in the dropdown menu
    else:
        status_var.set("Please fill in all fields")

# Function to search for questions
def search_question():
    category = category_var.get()
    search_term = search_entry.get().strip().lower()
    if category in qa_data and isinstance(qa_data[category], list):
        results = [q['question'] for q in qa_data[category] if search_term in q['question'].lower()]
        results_text = "\n".join(results) if results else "No questions found."
        search_results_label.config(text=results_text)
    else:
        search_results_label.config(text="No questions available for this category.")

# Load the data
qa_data = load_qa_data("new.json")

# Set up the GUI
root = tk.Tk()
root.title("Chatbot")

# Adjust the window size
root.geometry("500x500")

# Add a label for instructions
label = tk.Label(root, text="Please select a category:")
label.pack(pady=10)

category_var = tk.StringVar(root)
category_var.set("Select a category")

category_menu = tk.OptionMenu(root, category_var, "Select a category")
category_menu.pack(pady=
