from tkinter import *
from tkinter import messagebox
from ttkwidgets.autocomplete import AutocompleteEntry
from auxiliary import *
import time
import random
import os


projectDirectory, frenchDatabase = loadDirectories()
image = projectDirectory / "images/french_flag.png"
appSettings = projectDirectory / "settings.txt"


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
    with open(appSettings, "r") as file:
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
    new_seconds = int(newHours.get())*3600 + int(newMinutes.get())*60 + int(newSeconds.get())
    if new_seconds < 10:
        messagebox.showwarning('Exceeded time limit', 'Time should be set to at least 10 seconds!')
        return
    with open(appSettings, "r") as file:
        data = file.readlines()
    data[1] = 'hours = '
    if len(newHours.get()) == 0:
        data[1] += '0\n'
    else:
        data[1] += f'{newHours.get()}\n'
    data[2] = 'minutes = '
    if len(newMinutes.get()) == 0:
        data[2] += '0\n'
    else:
        data[2] += f'{newMinutes.get()}\n'
    data[3] = 'seconds = '
    if len(newSeconds.get()) == 0:
        data[3] += '0\n'
    else:
        data[3] += f'{newSeconds.get()}\n'
    with open(appSettings, 'w') as file:
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
    top.title(timeWindowTitle.get())
    Label(top, textvariable=mainMenuLabelText, font=("Arial", 18)).pack()
    Label(top, textvariable=hoursLabelText, width=6, anchor="w").place(x=89, y=timeLabel_y)
    Label(top, textvariable=minutesLabelText, width=6, anchor="w").place(x=167, y=timeLabel_y)
    Label(top, textvariable=secondsLabelText, width=6, anchor="w").place(x=250, y=timeLabel_y)
    newHours.set("{:0>0d}".format(int(hours.get())))
    newMinutes.set("{:0>0d}".format(int(minutes.get())))
    newSeconds.set("{:0>0d}".format(int(seconds.get())))
    Entry(top, textvariable=newHours, width=2, font=("Arial", 18)).place(x=57, y=timeLabel_y - 5)
    Entry(top, textvariable=newMinutes, width=2, font=("Arial", 18)).place(x=134, y=timeLabel_y - 5)
    Entry(top, textvariable=newSeconds, width=2, font=("Arial", 18)).place(x=217, y=timeLabel_y - 5)
    Button(top, textvariable=saveNewTimeButtonText, command=lambda: SaveTime(top)).place(x=130, y=timeLabel_y + 45)

    def on_closing():
        changeMainMenuState('active')
        top.destroy()

    top.protocol("WM_DELETE_WINDOW", on_closing)


def saveWordsSettings(window):
    results = availableWords()
    if len(results) == 0:
        messagebox.showwarning('no available words', 'you fucked up mate!')
    else:
        with open(appSettings, "r") as file:
            data = file.readlines()
        data[4] = f'category = {newCategory.get()}\n'
        data[5] = f'difficulty = {newDifficulty.get()}\n'
        data[6] = f'strict_tags = {newStrictTags.get()}\n'
        tags_number = len(newTagsList)
        for i in range(tags_number):
            if i < tags_number - 1:
                addition = '\n'
            else:
                addition = ''
            data[7 + i] = f'tag{i + 1} = {newTagsList[i].get()}{addition}'
        with open(appSettings, 'w') as file:
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
    newCategory.set(properCategoryList[0])
    newDifficulty.set(properDifficultiesList[0])
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
    Label(top, textvariable=setWordsConstraintsLabelText, font=("Arial", 18)).pack()
    Label(top, textvariable=wordCategoryLabelText).place(x=zero_x, y=55)
    Label(top, textvariable=tagsLabelText).place(x=zero_x, y=85)
    Label(top, textvariable=wordDifficultyLabelText).place(x=zero_x + 225, y=55)
    OptionMenu(top, newCategory, *properCategoryList).place(x=125, y=50)
    AutocompleteEntry(top, width=18, textvariable=newTag1, completevalues=availableLabels).place(x=50, y=85)
    AutocompleteEntry(top, width=18, textvariable=newTag2, completevalues=availableLabels).place(x=175, y=85)
    AutocompleteEntry(top, width=18, textvariable=newTag3, completevalues=availableLabels).place(x=300, y=85)
    AutocompleteEntry(top, width=18, textvariable=newTag4, completevalues=availableLabels).place(x=50, y=110)
    AutocompleteEntry(top, width=18, textvariable=newTag5, completevalues=availableLabels).place(x=175, y=110)
    AutocompleteEntry(top, width=18, textvariable=newTag6, completevalues=availableLabels).place(x=300, y=110)
    OptionMenu(top, newDifficulty, *properDifficultiesList).place(x=125 + 200, y=50)
    Button(top, textvariable=resetSettingsButtonText, command=resetNewSettingsVariables, width=14)\
        .place(x=350, y=timeLabel_y + 100)
    Button(top, textvariable=saveSettingButtonText, command=lambda: saveWordsSettings(top), width=14)\
        .place(x=177, y=timeLabel_y + 100)
    Checkbutton(top, textvariable=strictTagsLabelText, variable=newStrictTags).place(x=zero_x, y=135)

    def on_closing():
        changeMainMenuState('active')
        top.destroy()

    top.protocol("WM_DELETE_WINDOW", on_closing)


def showMainMenu():
    # labels
    mainMenuTimeLabel.pack()
    hoursLabel.place(x=89, y=timeLabel_y)
    minutesLabel.place(x=167, y=timeLabel_y)
    secondsLabel.place(x=250, y=timeLabel_y)
    hoursValueLabel.place(x=57, y=timeLabel_y - 5)
    minutesValueLabel.place(x=134, y=timeLabel_y - 5)
    secondsValueLabel.place(x=217, y=timeLabel_y - 5)
    # buttons
    startTimeButton.place(x=30, y=timeButtons_y)
    stopTimeButton.place(x=140, y=timeButtons_y)
    resetTimeButton.place(x=250, y=timeButtons_y)
    timeSettingsButton.place(x=70, y=settingsButtons_y)
    wordSettingsButton.place(x=200, y=settingsButtons_y)
    menuButton.place(x=250, y=settingsButtons_y+50)


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


def getEnglishCategory():
    category_value = newCategory.get()
    if category_value in polishCategoryList:
        category_value = polish_english_dictionary[category_value]
    return category_value


def getEnglishDifficulty():
    difficulty_value = newDifficulty.get().lower()
    if difficulty_value in polishDifficultiesList:
        difficulty_value = polish_english_dictionary[difficulty_value]
    return difficulty_value


def availableWords(target_database='all'):
    word_category = getEnglishCategory()
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
        select_query += f'difficulty == \'{getEnglishDifficulty():}\''
    select_query += ';'
    connection = sqlite3.connect(frenchDatabase)
    cursor = connection.cursor()
    available_words_list = []
    if database != 'all':
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
    game_window.title(gameTitle.get())
    game_window.attributes('-topmost', True)
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
            if language.get() == 'polish':
                temp_type_label = 'Typ słowa: ' + english_polish_dictionary[random_word[-1]]
            else:
                temp_type_label = 'Word type' + random_word[-1]
            word_type_label = Label(game_window, pady=10, font=("Arial", 18), text=temp_type_label)
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

            continue_game_button = Button(game_window, height=3, width=20, textvariable=continueGameLabelText,
                                          command=continueGameButtonAction)
            continue_game_button.place(x=35, y=160)
            stop_game_button = Button(game_window, height=3, width=20, textvariable=stopGameLabelText,
                                      command=stopGameButtonAction)
            stop_game_button.place(x=315, y=160)

            def wordDetailsButtonAction():

                def createDetailsWindow():
                    window = Toplevel(game_window)
                    window.title(detailsWindowName.get())
                    window.attributes('-topmost', True)
                    return window

                word_category = random_word[-1]
                if word_category in ['basic', 'adjective']:
                    messagebox.showinfo('No details', 'There are no details available for this word!')
                elif word_category == 'noun':
                    details_window = createDetailsWindow()
                    if language.get() == 'polish':
                        temp_word_gender = english_polish_dictionary[random_word[2]]
                    else:
                        temp_word_gender = random_word[2]
                    Label(details_window, text=f'{wordGenderLabelText.get()}: {temp_word_gender}').pack()
                elif word_category == 'verb':
                    details_window = createDetailsWindow()
                    conjugation_frame = LabelFrame(details_window)
                    conjugation_label = Label(conjugation_frame, textvariable=conjugationLabelText, pady=10,
                                              font=("Arial", 13), anchor='center')
                    conjugation_frame.pack(padx=20, pady=20)
                    conjugation_label.grid(row=0, column=0, columnspan=2)
                    Label(conjugation_frame, anchor="w", textvariable=singularLabelText, font=("Arial", 11))\
                        .grid(row=1, column=1)
                    Label(conjugation_frame, anchor="w", textvariable=pluralLabelText, font=("Arial", 11))\
                        .grid(row=1, column=2)
                    Label(conjugation_frame, anchor="e", textvariable=firstPersonLabelText, font=("Arial", 11)).grid(
                        row=2, column=0)
                    Label(conjugation_frame, anchor="e", textvariable=secondPersonLabelText, font=("Arial", 11)).grid(
                        row=3, column=0)
                    Label(conjugation_frame, anchor="e", textvariable=thirdPersonLabelText, font=("Arial", 11)).grid(
                        row=4, column=0)
                    Label(conjugation_frame, width=20, text=random_word[2], font=("Arial", 11)).grid(row=2, column=1)
                    Label(conjugation_frame, width=20, text=random_word[3], font=("Arial", 11)).grid(row=3, column=1)
                    Label(conjugation_frame, width=20, text=random_word[4], font=("Arial", 11)).grid(row=4, column=1)
                    Label(conjugation_frame, width=20, text=random_word[5], font=("Arial", 11)).grid(row=2, column=2)
                    Label(conjugation_frame, width=20, text=random_word[6], font=("Arial", 11)).grid(row=3, column=2)
                    Label(conjugation_frame, width=20, text=random_word[7], font=("Arial", 11)).grid(row=4, column=2)

            word_details_button = Button(game_window, height=2, width=10, textvariable=detailsWindowName,
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


def adjustToLanguage():
    global properCategoryList, properDifficultiesList, newCategory
    if language.get() == 'polish':
        properCategoryList = polishCategoryList
        properDifficultiesList = polishDifficultiesList
        for i in range(len(labelsList)):
            labelsList[i].set(english_polish_dictionary[labelsTextList[i]])
    else:
        properCategoryList = englishCategoryList
        properDifficultiesList = englishDifficultiesList
        for i in range(len(labelsList)):
            labelsList[i].set(labelsTextList[i])
    category.set(properCategoryList[0])


def openMenu():
    master.destroy()
    os.system('python french_learning.py')


master = Tk()
photo = PhotoImage(file=image)
master.iconphoto(True, photo)
master.title("Pop-up quiz")
master.geometry("360x250")

# Time things
hours = StringVar()
minutes = StringVar()
seconds = StringVar()
newHours = StringVar()
newMinutes = StringVar()
newSeconds = StringVar()
language = StringVar()
counting = False
playing = False
language.set(readLanguageFromFile())

# Words things
category = StringVar()
newCategory = StringVar()
englishCategoryList = ["all", "basic", "noun", "verb", "adjective"]
validWordCategoryList = ['basic', 'noun', 'verb', 'adjective']
polishCategoryList = ["wszystko", "podstawowe", "rzeczownik", "czasownik", "przymiotnik"]
properCategoryList = []
wordCategories = englishCategoryList[1:]
difficulty = StringVar()
newDifficulty = StringVar()
englishDifficultiesList = ["-", "easy", "normal", "hard"]
polishDifficultiesList = ['-', 'łatwe', 'średnie', 'trudne']
properDifficultiesList = []
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

conjugationLabelText = StringVar()
detailsWindowName = StringVar()
resetSettingsButtonText = StringVar()
saveSettingButtonText = StringVar()
setWordsConstraintsLabelText = StringVar()
wordCategoryLabelText = StringVar()
tagsLabelText = StringVar()
wordDifficultyLabelText = StringVar()
saveNewTimeButtonText = StringVar()
mainMenuLabelText = StringVar()
hoursLabelText = StringVar()
minutesLabelText = StringVar()
secondsLabelText = StringVar()
timeWindowTitle = StringVar()
gameTitle = StringVar()
strictTagsLabelText = StringVar()
timeUntilQuizLabelText = StringVar()
timeSettingLabelText = StringVar()
wordsSettingLabelText = StringVar()
continueGameLabelText = StringVar()
stopGameLabelText = StringVar()
singularLabelText = StringVar()
pluralLabelText = StringVar()
firstPersonLabelText = StringVar()
secondPersonLabelText = StringVar()
thirdPersonLabelText = StringVar()
wordGenderLabelText = StringVar()
labelsList = [conjugationLabelText, detailsWindowName, resetSettingsButtonText, saveSettingButtonText,
              setWordsConstraintsLabelText, wordCategoryLabelText, tagsLabelText, wordDifficultyLabelText,
              saveNewTimeButtonText, mainMenuLabelText, hoursLabelText, minutesLabelText, secondsLabelText,
              timeWindowTitle, gameTitle, strictTagsLabelText, timeUntilQuizLabelText, timeSettingLabelText,
              wordsSettingLabelText, continueGameLabelText, stopGameLabelText, singularLabelText, pluralLabelText,
              firstPersonLabelText, secondPersonLabelText, thirdPersonLabelText, wordGenderLabelText]
labelsTextList = ['Verb conjugation', 'Word \ndetails', 'Reset settings', 'Save new settings',
                  'Set available word constraints', 'Word category', 'Tags', 'Word difficulty', 'Save new time',
                  'Time between quizzes', 'hours', 'minutes', 'seconds', 'Time settings', 'Word quiz', 'Strict tags',
                  'Time until quiz', "Time settings", "Word settings", 'Continue game', 'Stop game', 'Singular',
                  'Plural', '1st person', '2nd person', '3rd person', 'Word gender']

# All things
settings = [language, hours, minutes, seconds, category, difficulty, strictTags, tag1, tag2, tag3, tag4, tag5, tag6]

english_polish_dictionary, polish_english_dictionary, allList, basicList, verbList, nounList, adjectiveList = \
    generateDictionariesAndLanLists()
availableLabels = createAvailableLabelsList(validWordCategoryList, tagsList)
availableLabels.remove(None)

# Set default values for variables
readSettingsFromFile()
prepareNewSettingsVariables()

# Master label setting
timeLabel_y = 55
mainMenuTimeLabel = Label(master, anchor='center', textvariable=timeUntilQuizLabelText, font=("Arial", 20))
hoursLabel = Label(master, textvariable=hoursLabelText, width=6, anchor="w")
minutesLabel = Label(master, textvariable=minutesLabelText, width=6, anchor="w")
secondsLabel = Label(master, textvariable=secondsLabelText, width=6, anchor="w")
hoursValueLabel = Label(master, textvariable=hours, width=2, font=("Arial", 18), anchor="e")
minutesValueLabel = Label(master, textvariable=minutes, width=2, font=("Arial", 18), anchor="e")
secondsValueLabel = Label(master, textvariable=seconds, width=2, font=("Arial", 18), anchor="e")

# Master button setting
buttonWidth = 13
timeButtons_y = timeLabel_y + 40
startTimeButton = Button(master, text="START", width=buttonWidth, pady=2, command=startCountdown, bg='#59E575')
stopTimeButton = Button(master, text="STOP", width=buttonWidth, pady=2, command=stopCountdown, bg='#E6978A')
resetTimeButton = Button(master, text="RESET", width=buttonWidth, pady=2, command=resetCountdown, bg='#BAFEFF')
settingsButtons_y = timeButtons_y + 50
timeSettingsButton = Button(master, textvariable=timeSettingLabelText, width=buttonWidth, pady=2,
                            command=openTimeSettings, bg='#C5D2EC')
wordSettingsButton = Button(master, textvariable=wordsSettingLabelText, width=buttonWidth, pady=2,
                            command=openWordsSettings, bg='#C5D2EC')
menuButton = Button(master, text="MENU", width=buttonWidth, pady=2, command=openMenu, bg='#C5D2EC')

master.protocol("WM_DELETE_WINDOW", onClosing)

adjustToLanguage()
showMainMenu()
master.mainloop()
