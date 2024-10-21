import tkinter as tk # Importing Tkinter as Tk instead of using from tkinter import * because i want to call tk later on as I make my classes
from tkinter import font # I wanna have good looking fonts
# Global Variable Library
Difficulty = ""


class Mainwindow(tk.Tk):  # Main window class
    def OnClick(self):
        self.btn["state"] = tk.DISABLED
        DiffWindow(self)  # Pass the instance of the main window

    def OnDestroy(self):
        self.btn["state"] = tk.ACTIVE  # Reactivate the button

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # Main Window Config
        self.title("Math Quiz")
        self.geometry("500x500")
        self.config(bg="#151515")

        title_font = font.Font(family="Helvetica", size=32, weight="bold")
        lbl = tk.Label(self, text="MATH QUIZ", bg="#151515", fg="#FFFFFF", pady=20, font=title_font)
        lbl.grid(row=0, column=0, columnspan=2)
        
        # Button for Difficulty selection
        self.btn = tk.Button(self, state="active", text="Difficulty Select!", bg="#151515", fg="#FFFFFF", padx=20, height=2, width=20, command=self.OnClick)
        self.btn.grid(row=1, column=0, padx=10, pady=10)

        # Button to play the game!
        play_btn = tk.Button(self, text="Play", bg="#151515", fg="#FFFFFF", padx=20, height=2, width=20)
        play_btn.grid(row=1, column=1, padx=10, pady=10)

        # Grid Weights for customization
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.mainloop()      
         
        
class DiffWindow(tk.Toplevel):
    def __init__(self, main_window, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, **kwargs)
        self.main_window = main_window  # I thought just using MainWindow class would work but after some digging through the tkinter handbook after getting multiple atr errors i found out that you have to reference the instance of the Main Window through the DiffWindow to make things work the way i wanted it to. 

        # Difficulty Window Configurations
        self.title("Difficulty Window")
        self.geometry("500x300")
        self.config(bg="#151515")
        
        self.difficulty_label = tk.Label(self, text="Select Difficulty", bg="#151515", fg="#FFFFFF", pady=20)
        self.difficulty_label.pack()
        
        easy_btn = tk.Button(self, text="Easy", command=self.set_easy, width=50, bg="#151515", fg="#FFFFFF", padx=20, pady=10)
        easy_btn.pack(pady=10)

        medium_btn = tk.Button(self, text="Medium", command=self.set_medium, width=50, bg="#151515", fg="#FFFFFF", padx=20, pady=10)
        medium_btn.pack(pady=10)

        hard_btn = tk.Button(self, text="Hard", command=self.set_hard, width=50, bg="#151515", fg="#FFFFFF", padx=20, pady=10)
        hard_btn.pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.OnClose)  # Detection of Window Closing and function to reactivate button
    
    # Functions to make the difficulty buttons work.
    def set_easy(self):
        global Difficulty
        Difficulty = "Easy"
        self.update_difficulty_label()
 
    def set_medium(self):
        global Difficulty
        Difficulty = "Medium"
        self.update_difficulty_label()

    def set_hard(self):
        global Difficulty
        Difficulty = "Hard"
        self.update_difficulty_label()
    
    # This one is to display what difficulty the player selected
    def update_difficulty_label(self):
        self.difficulty_label.config(text=f"Selected Difficulty: {Difficulty}")
    
    # Function to make the whole closing the window and reactivating the button work.
    def OnClose(self):
        self.main_window.OnDestroy()  # Calling the instance of the Main Window's Function which is "OnDestroy", to reactive the button
        self.destroy()


Mainwindow()