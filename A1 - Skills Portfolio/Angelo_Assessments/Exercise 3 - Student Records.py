import tkinter as tk
from tkinter import messagebox, simpledialog # Now to differentiate smy exercise 3 from my exercise 1... Im going to be using message boxes instead of new widows

class MainWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Student Records - Angelo School") # Just naming my school "Angelo School". I'm trying to be funny. Ha (HELP IM CRAMMING THIS)
        self.geometry("500x500")
        self.config(bg="#151515")
        
        self.Students = self.LoadStudents("A1 - Skills Portfolio\A1 - Resources\studentMarks.txt")
        
        self.CreateWidgets()
        
        self.mainloop()

    def LoadStudents(self, Filename): # This function uses file handling tech to load the file into useable data
        Students = [] # Very important array variable. It will contain everything we have
        with open("A1 - Skills Portfolio\A1 - Resources\studentMarks.txt", "r") as File:
            Lines = File.readlines() # This reads the lines and puts them into a variable
            Count = int(Lines[0].strip()) # This reads the first line which the count of the total students and turns that into a integer value so it can be used in the next line of code
            for Line in Lines[1:Count + 1]: # This reads every line starting from the second line. How? Well we have a count of how many students we have so I used that variable to create a loop that goes through each of them by using the range function! 
                Parts = Line.strip().split(",") # This just cleans up the lines. removing any spaces and seperating the stuff in the text file into a list so we can use the individual data and it not being just one big string
                StudentID = int(Parts[0]) # From the parts variable we take initial component and turn it into a integer becasue we know its the Student ID
                Name = Parts[1] # Similar to the one above but for the name. since we know the second component is always the name, we can specify that one in our Name variable and also not converting it into integer
                WorkMarks = list(map(int, Parts[2:5])) # Again similar from the first one but this time we know these 3 are all Work Grades so we can just batch them up into a list.
                ExamMark = int(Parts[5]) # we're seperating this one because it's the Exam Grade and we're going to use that for a different purpose later
                TotalWork = sum(WorkMarks) # Simple variable operation. just addin up all the integers in the WorkMarks list so we get the total grade of the works.
                TotalMarks = TotalWork + ExamMark # again another variable operation just adding to get the total grade overall
                Percentage = (TotalMarks / 160) * 100 # And then converting that grade into a percentage
                Grade = self.CalculateGrade(Percentage) # and then using that percentage in our function that makes it into a letter grade to finally put it in our Grade variable
                Students.append({ # Appending all this data into a array which is our "Students"
                    "StudentID": StudentID,
                    "Name": Name,
                    "Work": TotalWork,
                    "Exam": ExamMark,
                    "Total": TotalMarks,
                    "Percentage": Percentage,
                    "Grade": Grade
                })
        return Students

    def CalculateGrade(self, Percentage): # Simple function to calculate the grade and put it as a Letter grade
        if Percentage >= 70:
            return 'A'
        elif Percentage >= 60:
            return 'B'
        elif Percentage >= 50:
            return 'C'
        elif Percentage >= 40:
            return 'D'
        else:
            return 'F'

    def CreateWidgets(self): # I learnt this neat trick that you can basically just put all your widgets and whatnot into a function and call that function into your window!
        self.Menu = tk.Frame(self, bg="#151515")
        self.Menu.pack(pady=20)
        # This whole function contains all my buttons for the program
        tk.Button(self.Menu, text="View All Students", command=self.ViewAllStudents).pack(pady=5)
        tk.Button(self.Menu, text="View Individual Student", command=self.ViewIndividualStudent).pack(pady=5)
        tk.Button(self.Menu, text="Highest Total Score", command=self.HighestScore).pack(pady=5)
        tk.Button(self.Menu, text="Lowest Total Score", command=self.LowestScore).pack(pady=5)
        tk.Button(self.Menu, text="Sort Students", command=self.SortStudents).pack(pady=5)
        tk.Button(self.Menu, text="Add Student", command=self.AddStudent).pack(pady=5)
        tk.Button(self.Menu, text="Delete Student", command=self.DeleteStudent).pack(pady=5)
        tk.Button(self.Menu, text="Update Student", command=self.UpdateStudent).pack(pady=5)

    def ViewAllStudents(self):
        Records = "\n".join( # Using F strings as it should be. This is just us calling all the data we have from Students
            f"{S['Name']} (ID: {S['StudentID']}) - Total: {S['Total']}, Exam: {S['Exam']}, "
            f"Percentage: {S['Percentage']:.2f}%, Grade: {S['Grade']}"
            for S in self.Students # We're calling it here
        )
        Summary = f"Total Students: {len(self.Students)}\n" \
                  f"Average Percentage: {self.GetAveragePercentage():.2f}%"
        messagebox.showinfo("All Students", Records + "\n\n" + Summary)

    # All the functions below are pretty much self-explanatory just from the name alone. So i dont think i have to explain it? They're all just using the data and functions we have from above to display, update, create, and delete data from the array which is translated over from the text file.

    def ViewIndividualStudent(self):
        Name = simpledialog.askstring("Input", "Enter student name:")
        for Student in self.Students:
            if Student['Name'].lower() == Name.lower():
                self.ShowStudentInfo(Student)
                return
        messagebox.showerror("Error", "Student not found!")

    def HighestScore(self):
        Student = max(self.Students, key=lambda S: S['Total'])
        self.ShowStudentInfo(Student)

    def LowestScore(self):
        Student = min(self.Students, key=lambda S: S['Total'])
        self.ShowStudentInfo(Student)

    def ShowStudentInfo(self, Student):
        Info = (f"Name: {Student['Name']}\n"
                f"ID: {Student['StudentID']}\n"
                f"Total Work Marks: {Student['Work']}\n"
                f"Exam Marks: {Student['Exam']}\n"
                f"Overall Percentage: {Student['Percentage']:.2f}%\n"
                f"Grade: {Student['Grade']}")
        messagebox.showinfo("Student Info", Info)

    def SortStudents(self):
        Order = simpledialog.askstring("Input", "Sort by (Name/Total):")
        if Order not in ["Name", "Total"]:
            messagebox.showerror("Error", "Invalid sort option!")
            return
        Reverse = simpledialog.askstring("Input", "Sort order (asc/desc):")
        if Reverse == 'desc':
            self.Students.sort(key=lambda S: S[Order], reverse=True)
        else:
            self.Students.sort(key=lambda S: S[Order])
        messagebox.showinfo("Sorted Students", "Students sorted successfully!")

    def AddStudent(self):
        StudentID = simpledialog.askinteger("Input", "Enter student ID (1000-9999):")
        Name = simpledialog.askstring("Input", "Enter student name:")
        Marks = simpledialog.askstring("Input", "Enter Work marks (3 marks, separated by commas):")
        ExamMark = simpledialog.askinteger("Input", "Enter exam mark (0-100):")
        
        if not (1000 <= StudentID <= 9999) or not (0 <= ExamMark <= 100):
            messagebox.showerror("Error", "Invalid input!")
            return
        
        WorkMarks = list(map(int, Marks.split(",")))
        if len(WorkMarks) != 3 or any(M < 0 or M > 20 for M in WorkMarks):
            messagebox.showerror("Error", "Invalid Work marks!")
            return
        
        TotalWork = sum(WorkMarks)
        TotalMarks = TotalWork + ExamMark
        Percentage = (TotalMarks / 160) * 100
        Grade = self.CalculateGrade(Percentage)
        
        NewStudent = {
            "StudentID": StudentID,
            "Name": Name,
            "Work": TotalWork,
            "Exam": ExamMark,
            "Total": TotalMarks,
            "Percentage": Percentage,
            "Grade": Grade
        }
        
        self.Students.append(NewStudent)
        self.SaveStudents("studentMarks.txt")
        messagebox.showinfo("Success", "Student added successfully!")

    def DeleteStudent(self):
        Name = simpledialog.askstring("Input", "Enter student name to delete:")
        for Student in self.Students:
            if Student['Name'].lower() == Name.lower():
                self.Students.remove(Student)
                self.SaveStudents("studentMarks.txt")
                messagebox.showinfo("Success", "Student deleted successfully!")
                return
        messagebox.showerror("Error", "Student not found!")

    def UpdateStudent(self):
        Name = simpledialog.askstring("Input", "Enter student name to update:")
        for Student in self.Students:
            if Student['Name'].lower() == Name.lower():
                NewName = simpledialog.askstring("Input", "Enter new name (leave blank for no change):")
                NewMarks = simpledialog.askstring("Input", "Enter new Work marks (3 marks, separated by commas, leave blank for no change):")
                NewExamMark = simpledialog.askinteger("Input", "Enter new exam mark (0-100, leave blank for no change):")

                if NewName:
                    Student['Name'] = NewName
                if NewMarks:
                    WorkMarks = list(map(int, NewMarks.split(",")))
                    if len(WorkMarks) == 3 and all(0 <= M <= 20 for M in WorkMarks):
                        Student['Work'] = sum(WorkMarks)
                if NewExamMark is not None:
                    if 0 <= NewExamMark <= 100:
                        Student['Exam'] = NewExamMark

                # Recalculate totals
                Student['Total'] = Student['Work'] + Student['Exam']
                Student['Percentage'] = (Student['Total'] / 160) * 100
                Student['Grade'] = self.CalculateGrade(Student['Percentage'])

                self.SaveStudents("studentMarks.txt")
                messagebox.showinfo("Success", "Student updated successfully!")
                return
        messagebox.showerror("Error", "Student not found!")

    def GetAveragePercentage(self):
        TotalPercentage = sum(S['Percentage'] for S in self.Students)
        return TotalPercentage / len(self.Students) if self.Students else 0

    def SaveStudents(self, Filename):
        with open("A1 - Skills Portfolio\A1 - Resources\studentMarks.txt", "w") as File:
            File.write(f"{len(self.Students)}\n")
            for S in self.Students:
                File.write(f"{S['StudentID']},{S['Name']},{S['Work']},{S['Exam']}\n")

MainWindow()