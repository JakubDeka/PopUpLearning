from tkinter import *
import time
from tkinter import messagebox
import sqlite3
import random
from auxiliary import *
from pathlib import Path

project_directory = Path("D:/PythonProjects/frenchPopUp")
french_database = project_directory / "french_words.db"
image = project_directory / "images/french_flag.png"
app_settings = project_directory / "settings.txt"


def startCountdown():
    timeSettingsButton['state'] = 'disabled'
    wordSettingsButton['state'] = 'disabled'
    global counting
    counting = True
    remaining_time = 3600 * int(hours.get()) + 60 * int(minutes.get()) + int(seconds.get())
    while remaining_time >= 0 and counting:
        remaining_hours, remaining_minutes = divmod(remaining_time, 3600)
        remaining_minutes, remaining_seconds = divmod(remaining_minutes, 60)
        hours.set("{:0>2d}".format(remaining_hours))
        minutes.set("{:0>2d}".format(remaining_minutes))
        seconds.set("{:0>2d}".format(remaining_seconds))
        master.update()
        time.sleep(1)
        if remaining_time == 0:
            startTimeButton['state'] = 'disabled'
            stopTimeButton['state'] = 'disabled'
            resetTimeButton['state'] = 'disabled'
            playGame()
        remaining_time -= 1


def stopCountdown():
    global counting
    counting = False
    timeSettingsButton['state'] = 'active'
    wordSettingsButton['state'] = 'active'


def readSettingsFromFile():
    with open(app_settings, "r") as file:
        data = file.readlines()
    i = 0
    for line in data:
        value = line.split(' ')[-1].split('\n')[0]
        settings[i].set(value)
        i += 1
    formatTime()
    file.close()
    return


def SaveTime(window):
    with open(app_settings, "r") as file:
        data = file.readlines()
    data[0] = 'hours = '
    if len(newHours.get()) == 0:
        data[0] += '0\n'
    else:
        data[0] += f'{newHours.get()}\n'
    data[1] = 'minutes = '
    if len(newMinutes.get()) == 0:
        data[1] += '0\n'
    else:
        data[1] += f'{newMinutes.get()}\n'
    data[2] = 'seconds = '
    if len(newSeconds.get()) == 0:
        data[2] += '0\n'
    else:
        data[2] += f'{newSeconds.get()}\n'
    with open(app_settings, 'w') as file:
        file.writelines(data)
    readSettingsFromFile()
    window.destroy()
    changeMainMenuState('active')


def formatTime():
    hours.set("{:0>2d}".format(int(hours.get())))
    minutes.set("{:0>2d}".format(int(minutes.get())))
    seconds.set("{:0>2d}".format(int(seconds.get())))


def resetCountdown():
    stopCountdown()
    readSettingsFromFile()


def changeMainMenuState(state):
    startTimeButton['state'] = state
    stopTimeButton['state'] = state
    resetTimeButton['state'] = state
    timeSettingsButton['state'] = state
    wordSettingsButton['state'] = state


def openTimeSettings():
    changeMainMenuState('disabled')
    top = Toplevel(master)
    top.geometry("350x150")
    top.title("Time settings")
    Label(top, text='Set time between quizzes', font=("Arial", 18)).pack()
    Label(top, text=f'hours', width=6, anchor="w").place(x=99, y=timeLabel_y)
    Label(top, text=f'minutes', width=6, anchor="w").place(x=167, y=timeLabel_y)
    Label(top, text=f'seconds', width=6, anchor="w").place(x=250, y=timeLabel_y)
    newHours.set("{:0>0d}".format(int(hours.get())))
    newMinutes.set("{:0>0d}".format(int(minutes.get())))
    newSeconds.set("{:0>0d}".format(int(seconds.get())))
    Entry(top, textvariable=newHours, width=2, font=("Arial", 18)).place(x=67, y=timeLabel_y - 5)
    Entry(top, textvariable=newMinutes, width=2, font=("Arial", 18)).place(x=134, y=timeLabel_y - 5)
    Entry(top, textvariable=newSeconds, width=2, font=("Arial", 18)).place(x=217, y=timeLabel_y - 5)
    Button(top, text="Save new time", command=lambda: SaveTime(top)).place(x=130, y=timeLabel_y + 45)

    def on_closing():
        changeMainMenuState('active')
        top.destroy()

    top.protocol("WM_DELETE_WINDOW", on_closing)


def saveWordsSettings(window):
    results = availableWords()
    if len(results) == 0:
        messagebox.showwarning('no available words', 'you fucked up mate!')
    else:
        with open(app_settings, "r") as file:
            data = file.readlines()
        data[3] = f'category = {newCategory.get()}\n'
        data[4] = f'difficulty = {newDifficulty.get()}\n'
        data[5] = f'strict_tags = {newStrictTags.get()}\n'
        tags_number = len(newTagsList)
        for i in range(tags_number):
            if i < tags_number - 1:
                addition = '\n'
            else:
                addition = ''
            data[6 + i] = f'tag{i + 1} = {newTagsList[i].get()}{addition}'
        with open(app_settings, 'w') as file:
            file.writelines(data)
        readSettingsFromFile()
        window.destroy()
        changeMainMenuState('active')


def prepareNewSettingsVariables():
    newCategory.set(category.get())
    newDifficulty.set(difficulty.get())
    for i in range(len(newTagsList)):
        newTagsList[i].set(tagsList[i].get())
    newStrictTags.set(strictTags.get())


def resetNewSettingsVariables():
    newCategory.set('all')
    newDifficulty.set('-')
    for new_tag in newTagsList:
        new_tag.set('')
    newStrictTags.set(0)


def openWordsSettings():
    changeMainMenuState('disabled')
    prepareNewSettingsVariables()
    zero_x = 10
    top = Toplevel(master)
    top.geometry("470x200")
    top.title("Words settings")
    Label(top, text='Set available word constraints', font=("Arial", 18)).pack()
    Label(top, text="Word category").place(x=zero_x, y=55)
    Label(top, text="Tags:").place(x=zero_x, y=85)
    Label(top, text="Word difficulty").place(x=zero_x + 225, y=55)
    OptionMenu(top, newCategory, *categoryList).place(x=125, y=50)
    Entry(top, width=18, textvariable=newTag1).place(x=50, y=85)
    Entry(top, width=18, textvariable=newTag2).place(x=175, y=85)
    Entry(top, width=18, textvariable=newTag3).place(x=300, y=85)
    Entry(top, width=18, textvariable=newTag4).place(x=50, y=110)
    Entry(top, width=18, textvariable=newTag5).place(x=175, y=110)
    Entry(top, width=18, textvariable=newTag6).place(x=300, y=110)
    OptionMenu(top, newDifficulty, *difficulties).place(x=125 + 200, y=50)
    Button(top, text="Reset settings", command=resetNewSettingsVariables, width=10).place(x=350, y=timeLabel_y + 100)
    Button(top, text="Save new settings", command=lambda: saveWordsSettings(top), width=14).place(x=177,
                                                                                                  y=timeLabel_y + 100)
    Checkbutton(top, text='Strict tags', variable=newStrictTags).place(x=zero_x, y=135)

    def on_closing():
        changeMainMenuState('active')
        top.destroy()

    top.protocol("WM_DELETE_WINDOW", on_closing)


def showMainMenu():
    # labels
    mainMenuTimeLabel.pack()
    hoursLabel.place(x=99, y=timeLabel_y)
    minutesLabel.place(x=167, y=timeLabel_y)
    secondsLabel.place(x=250, y=timeLabel_y)
    hoursValueLabel.place(x=67, y=timeLabel_y - 5)
    minutesValueLabel.place(x=134, y=timeLabel_y - 5)
    secondsValueLabel.place(x=217, y=timeLabel_y - 5)
    # buttons
    startTimeButton.place(x=30, y=timeButtons_y)
    stopTimeButton.place(x=140, y=timeButtons_y)
    resetTimeButton.place(x=250, y=timeButtons_y)
    timeSettingsButton.place(x=70, y=settingsButtons_y)
    wordSettingsButton.place(x=200, y=settingsButtons_y)


def hideMainMenu():
    global counting
    counting = False
    # labels
    mainMenuTimeLabel.pack_forget()
    hoursLabel.place_forget()
    minutesLabel.place_forget()
    secondsLabel.place_forget()
    hoursValueLabel.place_forget()
    minutesValueLabel.place_forget()
    secondsValueLabel.place_forget()
    # buttons
    startTimeButton.place_forget()
    stopTimeButton.place_forget()
    resetTimeButton.place_forget()
    timeSettingsButton.place_forget()
    wordSettingsButton.place_forget()


def availableWords(target_database='all'):
    word_category = newCategory.get()
    if word_category == 'all':
        database = target_database
    else:
        database = word_category + "s"
    select_query = f'SELECT * FROM {database}'
    tag_words = createTagWordsList(newTagsList)
    tags_present = (len(tag_words) > 0)
    difficulty_present = (newDifficulty.get() != '-')
    if tags_present or difficulty_present:
        select_query += ' WHERE '
    if tags_present:
        tag_range = '\', \''.join(tag_words)
        select_query += f'tag1 in (\'{tag_range}\')'
        for i in range(1, len(newTagsList)):
            select_query += f' OR tag{i + 1} in (\'{tag_range}\')'
    if difficulty_present:
        if tags_present:
            select_query += ' AND '
        select_query += f'difficulty == \'{newDifficulty.get()}\''
    select_query += ';'
    connection = sqlite3.connect(french_database)
    cursor = connection.cursor()
    available_words_list = []
    if database != 'all':
        print(select_query)
        available_words_list = cursor.execute(select_query).fetchall()
        for i in range(len(available_words_list)):
            available_words_list[i] = list(available_words_list[i]) + [database[:-1]]
    else:
        for sub_category in wordCategories:
            sub_database = sub_category + 's'
            available_words_list += availableWords(target_database=sub_database)
    connection.commit()
    connection.close()
    # sieve for strict tags
    if strictTags.get():
        restrictWordsToStrictTags(available_words_list, tag_words)
    return available_words_list


def disappearButton(button):
    button.pack_forget()


def playGame():
    game_window = Toplevel(master)
    game_window.geometry("500x240")
    game_window.title("Word guessing")
    game_window.attributes('-topmost', True)
    word_info = ['pl', 'fr']
    pl_word = StringVar()
    pl_word.set(word_info[0])
    available_words_list = availableWords()

    def the_game(remaining_words_list):
        rounds_left = len(remaining_words_list)

        def stopGameButtonAction():
            game_window.destroy()
            changeMainMenuState('active')
            resetCountdown()
            startCountdown()

        if rounds_left == 0:
            messagebox.showinfo('No more words', 'There are no more words to be shown')
            stopGameButtonAction()
        else:
            random_word_index = random.randint(1, rounds_left)
            random_word = remaining_words_list.pop(random_word_index - 1)
            polish_word = random_word[0]
            french_word = random_word[1]

            def mainWordButtonAction(word_one, word_two):
                if main_word_button.cget('text') == word_one:
                    main_word_button['text'] = word_two
                else:
                    main_word_button['text'] = word_one

            main_word_text = StringVar()
            main_word_text.set(random_word[0])
            word_type_label = Label(game_window, font=("Arial", 18), text=random_word[-1])
            word_type_label.pack()
            main_word_button = Button(game_window, font=("Arial", 18), text=polish_word, height=3, width=30,
                                      command=lambda: mainWordButtonAction(polish_word, french_word))
            main_word_button.place(x=35, y=40)

            def continueGameButtonAction():
                for button in all_game_buttons:
                    button['state'] = 'disabled'
                answer = messagebox.askquestion('Skip word', 'Would you like to skip this word in this run?')
                if not answer:
                    remaining_words_list.append(random_word)
                try:
                    for button in all_game_buttons:
                        button.destroy()
                    word_type_label.pack_forget()
                    the_game(remaining_words_list)
                except TypeError:
                    return

            continue_game_button = Button(game_window, height=3, width=20, text='continue_game',
                                          command=continueGameButtonAction)
            continue_game_button.place(x=35, y=160)
            stop_game_button = Button(game_window, height=3, width=20, text='stop_game', command=stopGameButtonAction)
            stop_game_button.place(x=315, y=160)

            def wordDetailsButtonAction():

                def createDetailsWindow():
                    window = Toplevel(game_window)
                    window.title("Word guessing")
                    window.attributes('-topmost', True)
                    return window

                word_category = random_word[-1]
                print(word_category)
                if word_category in ['basic', 'adjective']:
                    messagebox.showinfo('No details', 'There are no details available for this word!')
                elif word_category == 'noun':
                    details_window = createDetailsWindow()
                    Label(details_window, text=f'Word gender: {random_word[2]}').pack()
                elif word_category == 'verb':
                    details_window = createDetailsWindow()
                    single_and_plural_y = 10
                    base_x = 10
                    singular_x = base_x + 70
                    plural_x = singular_x + 150
                    first_person_y = single_and_plural_y + 25
                    second_person_y = first_person_y + 25
                    third_person_y = second_person_y + 25
                    Label(details_window, anchor="w", text="Singular").place(x=singular_x, y=single_and_plural_y)
                    Label(details_window, anchor="w", text="Plural").place(x=plural_x, y=single_and_plural_y)
                    Label(details_window, anchor="e", text="1st person").place(x=base_x, y=first_person_y)
                    Label(details_window, anchor="e", text="2nd person").place(x=base_x, y=second_person_y)
                    Label(details_window, anchor="e", text="3rd person").place(x=base_x, y=third_person_y)
                    Label(details_window, anchor="w", width=20, text=random_word[2]).place(x=singular_x,
                                                                                           y=first_person_y)
                    Label(details_window, anchor="w", width=20, text=random_word[3]).place(x=singular_x,
                                                                                           y=second_person_y)
                    Label(details_window, anchor="w", width=20, text=random_word[4]).place(x=singular_x,
                                                                                           y=third_person_y)
                    Label(details_window, anchor="w", width=20, text=random_word[5]).place(x=plural_x, y=first_person_y)
                    Label(details_window, anchor="w", width=20, text=random_word[6]).place(x=plural_x,
                                                                                           y=second_person_y)
                    Label(details_window, anchor="w", width=20, text=random_word[7]).place(x=plural_x, y=third_person_y)
                    details_window.geometry('400x200')

            word_details_button = Button(game_window, height=2, width=10, text='Word\ndetails',
                                         command=wordDetailsButtonAction)
            word_details_button.place(x=207.5, y=160)
            all_game_buttons = [main_word_button, continue_game_button, stop_game_button, word_details_button]

    the_game(available_words_list)

    def on_closing():
        resetCountdown()
        changeMainMenuState('active')
        game_window.destroy()

    game_window.protocol("WM_DELETE_WINDOW", on_closing)


def onClosing():
    global counting
    counting = False
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        master.destroy()


master = Tk()
photo = PhotoImage(file=image)
master.iconphoto(True, photo)
master.title("Pop-up quiz")
master.geometry("360x200")

# Time things
hours = StringVar()
minutes = StringVar()
seconds = StringVar()
newHours = StringVar()
newMinutes = StringVar()
newSeconds = StringVar()
counting = False
playing = False

# Words things
category = StringVar()
newCategory = StringVar()
categoryList = ["all", "basic", "noun", "verb", "adjective"]
wordCategories = categoryList[1:]
difficulty = StringVar()
newDifficulty = StringVar()
difficulties = ["-", "easy", "normal", "hard"]
tag1 = StringVar()
tag2 = StringVar()
tag3 = StringVar()
tag4 = StringVar()
tag5 = StringVar()
tag6 = StringVar()
newTag1 = StringVar()
newTag2 = StringVar()
newTag3 = StringVar()
newTag4 = StringVar()
newTag5 = StringVar()
newTag6 = StringVar()
newTagsList = [newTag1, newTag2, newTag3, newTag4, newTag5, newTag6]
tagsList = [tag1, tag2, tag3, tag4, tag5, tag6]
strictTags = IntVar()
newStrictTags = IntVar()

# All things
settings = [hours, minutes, seconds, category, difficulty, strictTags, tag1, tag2, tag3, tag4, tag5, tag6]

# Set default values for variables
readSettingsFromFile()
prepareNewSettingsVariables()

# Master label setting
mainMenuTimeLabel = Label(master, anchor='center', text='Time until quiz', font=("Arial", 20))
timeLabel_y = 55
hoursLabel = Label(master, text=f'hours', width=6, anchor="w")
minutesLabel = Label(master, text=f'minutes', width=6, anchor="w")
secondsLabel = Label(master, text=f'seconds', width=6, anchor="w")
hoursValueLabel = Label(master, textvariable=hours, width=2, font=("Arial", 18), anchor="e")
minutesValueLabel = Label(master, textvariable=minutes, width=2, font=("Arial", 18), anchor="e")
secondsValueLabel = Label(master, textvariable=seconds, width=2, font=("Arial", 18), anchor="e")

# Master button setting
buttonWidth = 10
timeButtons_y = timeLabel_y + 40
startTimeButton = Button(master, text="START", width=buttonWidth, pady=2, command=startCountdown)
stopTimeButton = Button(master, text="STOP", width=buttonWidth, pady=2, command=stopCountdown)
resetTimeButton = Button(master, text="RESET", width=buttonWidth, pady=2, command=resetCountdown)
settingsButtons_y = timeButtons_y + 50
timeSettingsButton = Button(master, text="Time settings", width=buttonWidth, pady=2, command=openTimeSettings)
wordSettingsButton = Button(master, text="Word settings", width=buttonWidth, pady=2, command=openWordsSettings)

master.protocol("WM_DELETE_WINDOW", onClosing)
showMainMenu()
master.mainloop()
