import tkinter as tk # Once again importing tkinter as tk and not just using from tkinter import * because i need to call it in the class.
import random # Im importing the random library so i can randomize the selection of jokes

class Mainwindow(tk.Tk): # I'm just taking this from my Exercise 1. Im using classes and everything for my tkinter because i want to showcase my mastery over it
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title("Alexa")
        self.geometry("500x500")
        self.config(bg="#151515")
        
        self.jokes = self.load_jokes() # Loading the text file unto a variable so we can use it to randomize the selection of choices. It'll pop up in a function later
        self.CurrentJoke = None # Just a variable to store the joke strings
        
        self.Setup = tk.Label(self, text="", wraplength=400, bg="#151515", fg="white", font=("Helvetica", 14))
        self.Setup.pack(pady=20)

        self.Punchline = tk.Label(self, text="", wraplength=400, bg="#151515", fg="white", font=("Helvetica", 12))
        self.Punchline.pack(pady=20)

        self.PunchlineBtn = tk.Button(self, text="Show Punchline", command=self.show_punchline)
        self.PunchlineBtn.pack(pady=10)

        self.NextJokeBtn = tk.Button(self, text="Next Joke", command=self.next_joke)
        self.NextJokeBtn.pack(pady=10)

        self.Quit = tk.Button(self, text="Quit", command=self.quit)
        self.Quit.pack(pady=10)

        self.next_joke()  # This loads the jokes
        
        self.mainloop()
        
    def load_jokes(self): # As the variable name suggests this function loads the jokes using file handling methods
        with open("A1 - Skills Portfolio\\A1 - Resources\\randomJokes.txt", "r") as file: # this is our file handler! We're just loading the text file unto the variable file.
            return [line.strip() for line in file if line.strip()] # Then with this we strip the text file line by line!

    def next_joke(self): # This function cycles through the jokes from the loaded text file in the jokes variable
        self.CurrentJoke = random.choice(self.jokes)
        setup, _ = self.CurrentJoke.split('?', 1) # This makes it so that the setup and the punchline are seperated so that it wont show the punchline
        self.Setup.config(text=setup)
        self.Punchline.config(text="")
        
    def show_punchline(self):
        if self.CurrentJoke:
            _, punchline = self.CurrentJoke.split('?', 1) # This makes it so that the punchline is showed instead of the setup the reverse of the function above
            self.Punchline.config(text=punchline)
        
Mainwindow()