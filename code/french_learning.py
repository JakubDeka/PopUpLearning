from auxiliary import *
from tkinter import *
import os


def openDatabase():
    master.destroy()
    os.system('python database.py')


def openQuizApp():
    master.destroy()
    os.system('python quiz_app.py')


def adjustToLanguage():
    quizButtonText.set('Quiz')
    if language.get() == 'polish':
        databaseButtonText.set('Baza danych')
        windowTitle.set('Francuskie fiszki')
        changeLanguageText.set('polski')
    else:
        databaseButtonText.set('Database')
        windowTitle.set('French word flashcards')
        changeLanguageText.set('english')


def changeLanguage():
    if language.get() == 'english':
        language.set('polish')
    else:
        language.set('english')
    saveLanguageToFile(language.get())
    adjustToLanguage()


project_directory, french_database = loadDirectories()
image = project_directory / "images/french_flag.png"

master = Tk()
master.geometry("508x250")
photo = PhotoImage(file=image)
master.iconphoto(True, photo)
master.title("French learning menu")

language = StringVar()
language.set(readLanguageFromFile())
changeLanguageText = StringVar()
databaseButtonText = StringVar()
windowTitle = StringVar()
quizButtonText = StringVar()

menu = LabelFrame(master, padx=50, pady=50)
menu.grid(column=0, row=0, sticky=E+W, padx=0, pady=0)
Label(menu, width=25, textvariable=windowTitle, font=("Arial", 20)).grid(row=0, column=0, columnspan=2)
quizButton = Button(menu, width=10, textvariable=quizButtonText, command=openQuizApp, font=("Arial", 18))
quizButton.grid(row=1, column=0, pady=25)
dbButton = Button(menu, width=10, textvariable=databaseButtonText, command=openDatabase, font=("Arial", 18))
dbButton.grid(row=1, column=1)
changeLanguageButton = Button(menu, width=6, textvariable=changeLanguageText, command=changeLanguage)
changeLanguageButton.grid(row=2, column=1)

adjustToLanguage()
master.resizable(width=False, height=False)
master.mainloop()
