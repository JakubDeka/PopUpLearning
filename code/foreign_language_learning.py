from tkinter import ttk
from auxiliary import *
from tkinter import *
import os


def openDatabase():
    master.destroy()
    os.system('python database.py')


def openQuizApp():
    master.destroy()
    os.system('python quiz_app.py')


def initializeTaughtLanguagesList(language):
    if language.get() == 'english':
        available_taught_languages = ['english', 'french']
    else:
        available_taught_languages = ['angielski', 'francuski']
    return available_taught_languages


def adjustToLanguage():
    quizButtonText.set('Quiz')
    if language.get() == 'polish':
        databaseButtonText.set('Baza danych')
        languageText.set('Język')
        taughtLanguageText.set('Uczony język')
        if taughtLanguage.get() in ['french', 'francuski']:
            taughtLanguage.set('francuski')
            windowTitle.set('Francuskie fiszki')
        else:
            taughtLanguage.set('angielski')
            windowTitle.set('Angielskie fiszki')
        changeLanguageText.set('polski')
    else:
        databaseButtonText.set('Database')
        languageText.set('Language')
        taughtLanguageText.set('Taught language')
        windowTitle.set(f'{taughtLanguage.get()[0].upper()}{taughtLanguage.get()[1:]} flashcards')
        changeLanguageText.set('english')


def changeLanguage():
    if language.get() == 'english':
        if taughtLanguage.get() in ['english', 'angielski']:
            taughtLanguage.set('angielski')
        elif taughtLanguage.get() in ['french', 'francuski']:
            taughtLanguage.set('francuski')
        taughtLanguageComboBox['values'] = ['angielski', 'francuski']
        language.set('polish')
    else:
        if taughtLanguage.get() in ['english', 'angielski']:
            taughtLanguage.set('english')
        elif taughtLanguage.get() in ['french', 'francuski']:
            taughtLanguage.set('french')
        taughtLanguageComboBox['values'] = ['english', 'french']
        language.set('english')
    saveLanguageToFile(language.get())
    adjustToLanguage()


master = Tk()

taughtLanguage = StringVar()
taughtLanguage.set(readTaughtLanguageFromFile())

projectDirectory, foreignDatabase = loadDirectories(taughtLanguage.get())
image = projectDirectory / f"images/undefined_flag.png"

master.geometry("508x280")
photo = PhotoImage(file=image)
master.iconphoto(True, photo)
master.title(f"Pop-up learning")

language = StringVar()
language.set(readLanguageFromFile())

availableTaughtLanguages = initializeTaughtLanguagesList(language)

changeLanguageText = StringVar()
databaseButtonText = StringVar()
windowTitle = StringVar()
quizButtonText = StringVar()
languageText = StringVar()
taughtLanguageText = StringVar()

menu = LabelFrame(master, padx=50, pady=50)
menu.grid(column=0, row=0, sticky=E+W, padx=0, pady=0)
Label(menu, width=25, textvariable=windowTitle, font=("Arial", 20)).grid(row=0, column=0, columnspan=2)
quizButton = Button(menu, width=10, textvariable=quizButtonText, command=openQuizApp, font=("Arial", 18))
quizButton.grid(row=1, column=0, pady=25)
dbButton = Button(menu, width=10, textvariable=databaseButtonText, command=openDatabase, font=("Arial", 18))
dbButton.grid(row=1, column=1)
Label(menu, width=25, textvariable=taughtLanguageText, font=("Arial", 10)).grid(row=2, column=0)
Label(menu, width=25, textvariable=languageText, font=("Arial", 10)).grid(row=2, column=1)
taughtLanguageComboBox = ttk.Combobox(menu, textvariable=taughtLanguage, width=25, state='readonly',
                                      values=availableTaughtLanguages)
taughtLanguageComboBox.grid(row=3, column=0)


def saveTaughtLanguageToFile(event):
    with open(appSettings, "r") as file:
        data = file.readlines()
    if taughtLanguage.get() in ['french', 'francuski']:
        lang_to_write = 'french'
    elif taughtLanguage.get() in ['english', 'angielski']:
        lang_to_write = 'english'
    data[1] = f'taught_language = {lang_to_write}\n'
    with open(appSettings, 'w') as file:
        file.writelines(data)


taughtLanguageComboBox.bind("<<ComboboxSelected>>", func=saveTaughtLanguageToFile)
changeLanguageButton = Button(menu, width=6, textvariable=changeLanguageText, command=changeLanguage)
changeLanguageButton.grid(row=3, column=1)

adjustToLanguage()
master.resizable(width=False, height=False)
master.mainloop()
