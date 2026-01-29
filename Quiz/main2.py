import tkinter as tk

import json

import os

import random

 

DATA_FOLDER = "data"

 

def load_categories():

    categories = {}

    for filename in os.listdir(DATA_FOLDER):

        if filename.endswith(".json"):

            category_name = filename.replace(".json", "")

            with open(os.path.join(DATA_FOLDER, filename), "r", encoding="utf-8") as f:

                categories[category_name] = json.load(f)

    return categories

 

class QuizApp:

    def __init__(self, root):

        self.root = root

        root.title("Trivia Trainer")

 

        self.categories = load_categories()

        self.used_questions = set()

        self.current_question = None

        self.current_category = None

 

        self.main_frame = tk.Frame(root)

        self.main_frame.pack(fill="both", expand=True)

 

        self.show_category_screen()

 

    # ---------------- CATEGORY SCREEN ---------------- #

 

    def show_category_screen(self):

        self.clear_frame()

 

        tk.Label(self.main_frame, text="Choose a category:", font=("Arial", 16)).pack(pady=20)

 

        # Surprise me option

        tk.Button(self.main_frame, text="Surprise me!", font=("Arial", 14),

                  command=lambda: self.start_quiz("ALL")).pack(pady=5)

 

        # Individual categories

        for category in sorted(self.categories.keys()):

            tk.Button(self.main_frame, text=category, font=("Arial", 14),

                      command=lambda c=category: self.start_quiz(c)).pack(pady=5)

 

        tk.Button(self.main_frame, text="Exit", font=("Arial", 12),

                  command=self.root.quit).pack(pady=20)

 

    # ---------------- QUIZ LOGIC ---------------- #

 

    def start_quiz(self, category):

        self.current_category = category

        self.used_questions = set()

        self.show_question_screen()

 

    def get_question_pool(self):

        if self.current_category == "ALL":

            pool = []

            for cat in self.categories.values():

                pool.extend(cat)

            return pool

        return self.categories[self.current_category]

 

    def pick_question(self):

        pool = self.get_question_pool()

        available = [q for q in pool if q["question"] not in self.used_questions]

 

        if not available:

            return None

 

        q = random.choice(available)

        self.used_questions.add(q["question"])

        return q

 

    # ---------------- QUESTION SCREEN ---------------- #

 

    def show_question_screen(self):

        self.clear_frame()

 

        self.current_question = self.pick_question()

 

        if not self.current_question:

            tk.Label(self.main_frame, text="No more questions in this category!",

                     font=("Arial", 14)).pack(pady=20)

            tk.Button(self.main_frame, text="Back to categories",

                      command=self.show_category_screen).pack(pady=10)

            return

 

        tk.Label(self.main_frame, text=self.current_question["question"],

                 wraplength=500, font=("Arial", 16)).pack(pady=20)

 

        self.answer_label = tk.Label(self.main_frame, text="", wraplength=500,

                                     font=("Arial", 14), fg="blue")

        self.answer_label.pack(pady=10)

 

        self.info_label = tk.Label(self.main_frame, text="", wraplength=500,

                                   font=("Arial", 12), fg="green")

        self.info_label.pack(pady=10)

 

        tk.Button(self.main_frame, text="Reveal answer", font=("Arial", 12),

                  command=self.reveal_answer).pack(pady=5)

 

        tk.Button(self.main_frame, text="More information", font=("Arial", 12),

                  command=self.show_info).pack(pady=5)

 

        tk.Button(self.main_frame, text="Next question", font=("Arial", 12),

                  command=self.show_question_screen).pack(pady=5)

 

        tk.Button(self.main_frame, text="Back", font=("Arial", 12),

                  command=self.show_category_screen).pack(pady=15)

 

        tk.Button(self.main_frame, text="Exit", font=("Arial", 12),

                  command=self.root.quit).pack()

 

    def reveal_answer(self):

        self.answer_label.config(text=self.current_question["answer"])

 

    def show_info(self):

        info = self.current_question.get("info", "No additional information available.")

        self.info_label.config(text=info)

 

    # ---------------- UTIL ---------------- #

 

    def clear_frame(self):

        for widget in self.main_frame.winfo_children():

            widget.destroy()

 

# ---------------- RUN APP ---------------- #

 

root = tk.Tk()

app = QuizApp(root)

root.mainloop()
