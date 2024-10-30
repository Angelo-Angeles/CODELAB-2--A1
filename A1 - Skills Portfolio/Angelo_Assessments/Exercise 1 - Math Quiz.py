import tkinter as tk  # Importing Tkinter as Tk for class calls cause apparently i need em
from tkinter import font  # Importing font for styling text
import random  # Importing random for generating random numbers

Difficulty = ""  # Variable to store selected difficulty level


class Mainwindow(tk.Tk):  # Main window class
    def OnClickDiff(self): # Disable the button and open the difficulty selection window.
        self.btn["state"] = tk.DISABLED
        DiffWindow(self)  # Instantiate the difficulty selection window
        
    def OnClickPlay(self): # Disable the button and start the quiz if a difficulty is selected.
        if Difficulty:
            self.btn["state"] = tk.DISABLED
            QuizWindow(self, Difficulty)  # Instantiate the quiz window

    def OnDestroy(self): # Reactivate the difficulty button when the quiz is closed.
        self.btn["state"] = tk.ACTIVE

    def __init__(self, *args, **kwargs): # Initialize the main window and its components.
        tk.Tk.__init__(self, *args, **kwargs)
        
        # Main Window Config
        self.title("Math Quiz") 
        self.geometry("500x500")
        self.config(bg="#151515")

        title_font = font.Font(family="Helvetica", size=32, weight="bold")  # Define title font
        lbl = tk.Label(self, text="MATH QUIZ", bg="#151515", fg="#FFFFFF", pady=20, font=title_font)
        lbl.grid(row=0, column=0, columnspan=2)  # Adds the Title
        
        # Button for Difficulty selection
        self.btn = tk.Button(self, state="active", text="Difficulty Select!", bg="#151515", fg="#FFFFFF", padx=20, height=2, width=20, command=self.OnClickDiff)
        self.btn.grid(row=1, column=0, padx=10, pady=10)  # Add the difficulty button

        # Button to play the game
        self.play_btn = tk.Button(self, text="Play", bg="#151515", fg="#FFFFFF", padx=20, height=2, width=20, command=self.OnClickPlay)
        self.play_btn.grid(row=1, column=1, padx=10, pady=10)  # Add the play button (No not the YT Play Button)

        # Grid Weights for customization
        self.grid_rowconfigure(0, weight=1)  # Configure row weights
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)  # Configure column weights
        self.grid_columnconfigure(1, weight=1)

        self.mainloop()


class DiffWindow(tk.Toplevel):
    def __init__(self, main_window, *args, **kwargs):
        """Initialize the difficulty selection window."""
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.main_window = main_window  # Reference to the main window

        # Difficulty Window Configurations
        self.title("Difficulty Window")  # Set the window title
        self.geometry("500x320")  # Set the window size
        self.config(bg="#151515")  # Set the background color
        
        self.difficulty_label = tk.Label(self, text="Select Difficulty", bg="#151515", fg="#FFFFFF", pady=20)
        self.difficulty_label.pack()  # Add label to select difficulty
        
        # Create difficulty buttons
        easy_btn = tk.Button(self, text="Easy", command=self.set_easy, width=50, bg="#151515", fg="#FFFFFF", padx=20, pady=10)
        easy_btn.pack(pady=10)  # Add Easy button

        normal_btn = tk.Button(self, text="Normal", command=self.set_normal, width=50, bg="#151515", fg="#FFFFFF", padx=20, pady=10)
        normal_btn.pack(pady=10)  # Add Normal button

        difficult_btn = tk.Button(self, text="Difficult", command=self.set_difficult, width=50, bg="#151515", fg="#FFFFFF", padx=20, pady=10)
        difficult_btn.pack(pady=10)  # Add Difficult button

        impossible_btn = tk.Button(self, text="Impossible", command=self.set_impossible, width=50, bg="#151515", fg="#FFFFFF", padx=20, pady=10)
        impossible_btn.pack(pady=10)  # Add Impossible button

        self.protocol("WM_DELETE_WINDOW", self.OnClose)  # Handle window close event

    def set_easy(self):
        """Set the difficulty to Easy and update the label."""
        global Difficulty
        Difficulty = "Easy"
        self.update_difficulty_label()

    def set_normal(self):
        """Set the difficulty to Normal and update the label."""
        global Difficulty
        Difficulty = "Normal"
        self.update_difficulty_label()

    def set_difficult(self):
        """Set the difficulty to Difficult and update the label."""
        global Difficulty
        Difficulty = "Difficult"
        self.update_difficulty_label()

    def set_impossible(self):
        """Set the difficulty to Impossible and update the label."""
        global Difficulty
        Difficulty = "Impossible"
        self.update_difficulty_label()

    def update_difficulty_label(self):
        """Update the label to display the selected difficulty."""
        self.difficulty_label.config(text=f"Selected Difficulty: {Difficulty}")

    def OnClose(self):
        """Handle closing of the difficulty window and reactivate the main window button."""
        self.main_window.OnDestroy()
        self.destroy()  # Close the difficulty window


class QuizWindow(tk.Toplevel):
    def __init__(self, main_window, Difficulty):
        super().__init__()
        
        self.main_window = main_window  # Reference to the main window
        self.Difficulty = Difficulty
        self.score = 0  # This is just the score variable
        self.question_count = 0  # Yeah this is just the variable to count how many questions there are
        self.max_questions = 10  # Set the maximum number of questions
        self.attempts = 0  # The variable to store the amount of attempts attempted

        self.title("Quiz")  # Set the quiz window title
        self.geometry("600x300")  # Set the window size
        self.config(bg="#151515")  # Set the background color

        question_font = font.Font(family="Helvetica", size=20)
        
        self.question_label = tk.Label(self, bg="#151515", fg="#FFFFFF", font=question_font)
        self.question_label.pack(pady=20)  

        self.answer_entry = tk.Entry(self, font=question_font)
        self.answer_entry.pack(pady=10)  

        self.submit_btn = tk.Button(self, text="Submit", command=self.check_answer, bg="#151515", fg="#FFFFFF")
        self.submit_btn.pack(pady=10)  

        self.next_question()  # Load the first question
        self.protocol("WM_DELETE_WINDOW", self.OnClose) 
    
    def OnClose(self):
        self.main_window.OnDestroy()
        self.destroy()  # Close the quiz window

    def random_int(self): # Generate a random integer based on the selected difficulty.
        if self.Difficulty == "Easy":
            return random.randint(0, 9)
        elif self.Difficulty == "Normal":
            return random.randint(10, 99)
        elif self.Difficulty == "Difficult":
            return random.randint(100, 999) 
        elif self.Difficulty == "Impossible":
            return random.randint(1000, 9999)

    def decide_operation(self): # Randomly select an arithmetic operation.
        return random.choice(['+', '-', '*', '/'])

    def next_question(self): # Load the next question or display results if all questions have been answered.
        if self.question_count < self.max_questions:
            self.num1 = self.random_int()  # Generate the first random number
            self.num2 = self.random_int()  # Generate the second random number
            self.operation = self.decide_operation()  # Determines the operation used in the question
            self.question_label.config(text=f"{self.num1} {self.operation} {self.num2} = ?") 
            self.answer_entry.delete(0, tk.END)  # Clear the answer entry
            self.attempts = 0  # Reset the attempts variable
        else:
            self.display_results()  # Show the results if questions are completed

    def check_answer(self): # Check the user's answer and update the score and question count
        try:
            user_answer = int(self.answer_entry.get())  # Get the user's answer
            correct_answer = eval(f"{self.num1} {self.operation} {self.num2}")  # Calculate the correct answer

            if self.attempts == 0:  # First attempt
                if user_answer == correct_answer:
                    self.score += 10  # Add to score for correct answer
                    self.question_count += 1  # Move to the next question
                    self.next_question()
                else:
                    self.question_label.config(text="Incorrect! Try again.")  # Prompt for retry
                    self.attempts += 1  # Adds 1 to the attempt counter
                    self.answer_entry.delete(0, tk.END)  # Clear the answer entry
            else:  # Second attempt
                if user_answer == correct_answer:
                    self.score += 5  # Add to score for correct answer
                    self.question_count += 1  # Move to the next question
                    self.next_question()
                else:
                    self.question_label.config(text=f"Incorrect! The correct answer was {correct_answer}.")  # Show correct answer
                    self.question_count += 1  # Move to the next question
                    self.attempts = 0  # Reset Attempt variable
                    self.after(2000, self.next_question)  # Delay before next question (Cause ya know its cooler than a button)
        except ValueError:
            self.question_label.config(text="Please enter a valid number.")  # Prompt for valid input (incase someone decides to input something other than a button)

    def display_results(self): # Display the user's score and grade after completing the quiz.
        result = f"Your score: {self.score} / 100"
        if self.score >= 90:
            result += "\nGrade: A+"
        elif self.score >= 80:
            result += "\nGrade: A"
        elif self.score >= 70:
            result += "\nGrade: B"
        elif self.score >= 60:
            result += "\nGrade: C"
        else:
            result += "\nGrade: F"

        self.question_label.config(text=result)  # Update the label with results
        self.answer_entry.destroy()  # Remove the answer entry field
        self.submit_btn.destroy()  # Remove the submit button
        
        # Add Retry button
        retry_btn = tk.Button(self, text="Retry", command=self.retry_quiz, bg="#151515", fg="#FFFFFF")
        retry_btn.pack(pady=10)  # Add the Retry button

    def retry_quiz(self): # Reset the quiz variables and start a new quiz.
        self.score = 0  # Reset the score
        self.question_count = 0  # Reset the question count
        self.attempts = 0  # Reset attempts
        self.next_question()


Mainwindow()