from auxiliary import *
from tkinter import *
import os


def openDatabase():
    os.system('python database.py')


def openQuizApp():
    os.system('python quiz_app.py')


project_directory, french_database = loadDirectories()
image = project_directory / "images/french_flag.png"

master = Tk()
master.geometry("320x150")
photo = PhotoImage(file=image)
master.iconphoto(True, photo)
master.title("French learning menu")

language = readLanguageFromFile()
quizButtonText = 'Quiz'
if language == 'polish':
    databaseButtonText = 'Baza danych'
    windowTitle = 'Francuskie fiszki'
else:
    databaseButtonText = 'Database'
    windowTitle = 'French word flashcards'

Label(master, text=windowTitle, font=("Arial", 20)).grid(row=0, column=0, columnspan=2, pady=15, padx=55)
Button(master, text=quizButtonText, command=openQuizApp, font=("Arial", 18)).grid(row=1, column=0)
Button(master, text=databaseButtonText, command=openDatabase, font=("Arial", 18)).grid(row=1, column=1)

master.resizable(width=False, height=False)
master.mainloop()
