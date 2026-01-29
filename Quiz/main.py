import tkinter as tk

from tkinter import ttk

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

        root.geometry("700x500")

 

        # ttk theme

        style = ttk.Style()

        style.theme_use("clam")

 

        # Light blue background

        self.bg = "#cfe8ff"

 

        # Button styles

        style.configure(

            "Category.TButton",

            font=("Arial", 16),

            padding=10,

            background="#ffffff",

            foreground="#000000"

        )

 

        style.map(

            "Category.TButton",

            background=[("active", "#e0e0e0")]

        )

 

        style.configure(

            "Action.TButton",

            font=("Arial", 16),

            padding=10,

            background="#4a90e2",

            foreground="white"

        )

 

        style.map(

            "Action.TButton",

            background=[("active", "#357ABD")]

        )

 

        style.configure(

            "Secondary.TButton",

            font=("Arial", 14),

            padding=8,

            background="#dddddd",

            foreground="black"

        )

 

        style.configure(

            "Exit.TButton",

            font=("Arial", 14),

            padding=10,

            background="#b00020",

            foreground="white"

        )

 

        style.map(

            "Exit.TButton",

            background=[("active", "#8a0019")]

        )

 

        self.categories = load_categories()

        self.used_questions = set()

        self.current_question = None

        self.current_category = None

 

        self.main_frame = tk.Frame(root, bg=self.bg)

        self.main_frame.pack(fill="both", expand=True)

 

        self.show_category_screen()

 

    # ---------------- CATEGORY SCREEN ---------------- #

 

    def show_category_screen(self):

        self.clear_frame()

 

        tk.Label(

            self.main_frame,

            text="Choose a category",

            font=("Arial", 26),

            bg=self.bg

        ).pack(pady=25)

 

        # Surprise me

        ttk.Button(

            self.main_frame,

            text="Surprise me!",

            style="Action.TButton",

            command=lambda c="ALL": self.start_quiz(c)

        ).pack(pady=10)

 

        # Category buttons

        for category in sorted(self.categories.keys()):

            ttk.Button(

                self.main_frame,

                text=category,

                style="Category.TButton",

                command=lambda c=category: self.start_quiz(c)

            ).pack(pady=8)

 

        ttk.Button(

            self.main_frame,

            text="Exit",

            style="Exit.TButton",

            command=self.root.quit

        ).pack(pady=25)

 

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

            tk.Label(

                self.main_frame,

                text="No more questions in this category!",

                font=("Arial", 20),

                bg=self.bg

            ).pack(pady=20)

 

            ttk.Button(

                self.main_frame,

                text="Back to categories",

                style="Action.TButton",

                command=self.show_category_screen

            ).pack(pady=10)

            return

 

        # Question text

        tk.Label(

            self.main_frame,

            text=self.current_question["question"],

            wraplength=600,

            font=("Arial", 22),

            bg=self.bg

        ).pack(pady=25)

 

        # Answer + info labels

        self.answer_label = tk.Label(

            self.main_frame,

            text="",

            wraplength=600,

            font=("Arial", 18),

            fg="#004a99",

            bg=self.bg

        )

        self.answer_label.pack(pady=10)

 

        self.info_label = tk.Label(

            self.main_frame,

            text="",

            wraplength=600,

            font=("Arial", 16),

            fg="#006622",

            bg=self.bg

        )

        self.info_label.pack(pady=10)

 

        # Action buttons (side by side)

        action_frame = tk.Frame(self.main_frame, bg=self.bg)

        action_frame.pack(pady=10)

 

        ttk.Button(

            action_frame,

            text="Reveal Answer",

            style="Action.TButton",

            command=self.reveal_answer

        ).grid(row=0, column=0, padx=15)

 

        ttk.Button(

            action_frame,

            text="Next Question",

            style="Category.TButton",

            command=self.show_question_screen

        ).grid(row=0, column=1, padx=15)

 

        # More information button (centered)

        ttk.Button(

            self.main_frame,

            text="More information",

            style="Secondary.TButton",

            command=self.show_info

        ).pack(pady=10)

 

        # Bottom navigation

        bottom_frame = tk.Frame(self.main_frame, bg=self.bg)

        bottom_frame.pack(fill="x", pady=25)

 

        ttk.Button(

            bottom_frame,

            text="Back",

            style="Category.TButton",

            command=self.show_category_screen

        ).pack(side="left", padx=20)

 

        ttk.Button(

            bottom_frame,

            text="Exit",

            style="Exit.TButton",

            command=self.root.quit

        ).pack(side="right", padx=20)

 

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


