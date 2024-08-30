import tkinter as tk
import json

# Load questions and answers from the JSON file
def load_qa_data(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
            print("JSON data loaded successfully!")
            return data
    except Exception as e:
        print(f"Error loading JSON data: {e}")
        return {}

# Function to update the category dropdown
def update_categories():
    categories = list(qa_data.keys())
    category_menu["menu"].delete(0, "end")
    for category in categories:
        category_menu["menu"].add_command(label=category, command=tk._setit(category_var, category))

# Function to update the questions based on the selected category
def update_questions(*args):
    selected_category = category_var.get()
    if selected_category in qa_data:
        question_list.delete(0, tk.END)  # Clear the listbox
        for index, qa in enumerate(qa_data[selected_category]):
            question_text = f"{index + 1}. {qa['question']}"
            question_list.insert(tk.END, question_text)

# Function to show the answer when a question is selected
def show_answer(event):
    selected_index = question_list.curselection()
    if selected_index:
        selected_question = selected_index[0]
        selected_category = category_var.get()
        answer_text.delete(1.0, tk.END)
        answer = qa_data[selected_category][selected_question]['answer']
        answer_text.insert(tk.END, answer)

# Function to add a new question
def add_question():
    category = category_var.get()
    if category and category in qa_data:
        question = new_question_entry.get()
        answer = new_answer_entry.get()
        if question and answer:
            qa_data[category].append({"question": question, "answer": answer})
            with open("new.json", "w", encoding="utf-8") as file:
                json.dump(qa_data, file, indent=4)
            update_questions()  # Refresh the question list to include the new question
            new_question_entry.delete(0, tk.END)
            new_answer_entry.delete(0, tk.END)
            print(f"Added new question: {question}")

# Load the data
qa_data = load_qa_data("new.json")

# Set up the GUI
root = tk.Tk()
root.title("Chatbot")

# Maximize the window
root.geometry("1000x800")  # Adjust the window size

# Set font for labels and buttons
font_large = ("Arial", 14)
font_medium = ("Arial", 12)

# Category selection
category_label = tk.Label(root, text="Select Category:", font=font_large)
category_label.pack(pady=10)

category_var = tk.StringVar(root)
category_var.trace("w", update_questions)
category_menu = tk.OptionMenu(root, category_var, "Select a category")
category_menu.config(font=font_large)
category_menu.pack(pady=10)

# Frame for the Listbox and Text widgets
listbox_frame = tk.Frame(root)
listbox_frame.pack(pady=10, padx=20, fill=tk.BOTH, expand=True)

# Questions list
question_list = tk.Listbox(listbox_frame, height=15, width=60, font=font_medium)
question_list.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, expand=True)
question_list.bind("<<ListboxSelect>>", show_answer)

# Answers text
answer_text = tk.Text(listbox_frame, height=10, width=60, font=font_medium, fg="blue", wrap=tk.WORD)
answer_text.pack(side=tk.TOP, padx=10, pady=10, fill=tk.BOTH, expand=True)

# Add new question
new_question_label = tk.Label(root, text="New Question:", font=font_large)
new_question_label.pack(pady=5)
new_question_entry = tk.Entry(root, width=100, font=font_medium)
new_question_entry.pack(pady=5)

new_answer_label = tk.Label(root, text="New Answer:", font=font_large)
new_answer_label.pack(pady=5)
new_answer_entry = tk.Entry(root, width=100, font=font_medium)
new_answer_entry.pack(pady=5)

add_question_button = tk.Button(root, text="Add Question", command=add_question, font=font_large)
add_question_button.pack(pady=10)

# Call the function to update the categories in the dropdown
update_categories()

root.mainloop()
