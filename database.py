from tkinter import *
import sqlite3
from tkinter import messagebox


def HideVerbPersons():
    for i in range(len(verbLabelsList)):
        verbLabelsList[i].place_forget()
        verbEntryList[i].place_forget()


def ShowAppropriateEntries(master):
    base_y = 160
    first_row_y = base_y + 25
    second_row_y = first_row_y + 25
    third_row_y = second_row_y + 25
    word_type = wordCategory.get()
    if word_type == "noun":
        # Show
        frenchGenderLabel.place(x=zero_x, y=base_y + 5)
        frenchGender.place(x=first_x, y=base_y)
        # Hide
        verbSingularLabel.place_forget()
        verbPluralLabel.place_forget()
        HideVerbPersons()
    elif word_type == "verb":
        # Show
        verbSingularLabel.place(x=first_x, y=base_y)
        firstPersonLabel.place(x=zero_x, y=first_row_y)
        firstPerson.place(x=first_x, y=first_row_y)
        secondPersonLabel.place(x=zero_x, y=second_row_y)
        secondPerson.place(x=first_x, y=second_row_y)
        thirdPersonLabel.place(x=zero_x, y=third_row_y)
        thirdPerson.place(x=first_x, y=third_row_y)
        verbPluralLabel.place(x=second_x, y=base_y)
        fourthPerson.place(x=second_x, y=first_row_y)
        fifthPerson.place(x=second_x, y=second_row_y)
        sixthPerson.place(x=second_x, y=third_row_y)
        # Hide
        frenchGenderLabel.place_forget()
        frenchGender.place_forget()
    else:
        # Hide
        frenchGenderLabel.place_forget()
        frenchGender.place_forget()
        verbSingularLabel.place_forget()
        verbPluralLabel.place_forget()
        HideVerbPersons()


def checkIfKeyEntriesFilled():
    if (len(polishWordEntry.get()) > 0) & (len(frenchWordEntry.get()) > 0):
        return True
    return False


def createFoundWordsWindow(no_words=1, no_tables=1):
    top = Toplevel(master)
    top.geometry(f"550x{(no_tables + no_words) * 40}")
    top.title("Found words")
    return top


def selectFoundWord(window, text):
    enableButtons()
    enableEntriesAndDropdown()
    words = text.split()
    if text[2] == 'A':
        database = 'adjectives'
    elif text[2] == 'B':
        database = 'basics'
    elif text[2] == 'N':
        database = 'nouns'
    else:
        database = 'verbs'
    oid = words[1][:-1]
    connection = sqlite3.connect("french_words.db")
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {database} WHERE oid == {oid}")
    result = list(cursor.fetchmany(1)[0])
    for i in range(len(result)):
        if result[i] is None:
            result[i] = ''
    polish_word.set(result[0])
    french_word.set(result[1])
    tag1.set(result[-4])
    tag2.set(result[-3])
    tag3.set(result[-2])
    wordDifficulty.set(result[-1])
    if database == 'nouns':
        nounGender.set(result[2])
    elif database == 'verbs':
        first_person.set(result[2])
        second_person.set(result[3])
        third_person.set(result[4])
        fourth_person.set(result[5])
        fifth_person.set(result[6])
        sixth_person.set(result[7])
    connection.commit()
    connection.close()
    window.destroy()


def findWord():
    if wordCategory.get() == 'all':
        messagebox.showwarning("missing data", "You NEED to select one of the available WORD CATEGORY!")
        return
    database = wordCategory.get() + "s"
    connection = sqlite3.connect("french_words.db")
    cursor = connection.cursor()
    cursor.execute(f'select * from {database} LIMIT 1;')
    names = [description[0] for description in cursor.description]
    query = f'SELECT {names[0]}, {names[1]}, oid FROM {database}'
    tag_words = createTagWordList()
    if (wordDifficulty.get() != '-') | (len(tag_words) > 0) | (len(polishWordEntry.get()) > 0) | (
            len(frenchWordEntry.get()) > 0):
        query += ' WHERE '
    no_conditions = 0
    # query condition for names
    if checkIfKeyEntriesFilled():
        query += f'({names[0]}==\'{polishWordEntry.get()}\' AND {names[1]}==\'{frenchWordEntry.get()}\')'
        no_conditions += 1
    elif (len(polishWordEntry.get()) > 0) | (len(frenchWordEntry.get()) > 0):
        query += f'({names[0]}==\'{polishWordEntry.get()}\' OR {names[1]}==\'{frenchWordEntry.get()}\')'
        no_conditions += 1
    # query condition for tags
    # add exclusive tags ('and' instead of 'or')
    if len(tag_words) > 0:
        query, no_conditions = addTagsToQuery(no_conditions, query, tag_words)
    if wordDifficulty.get() != '-':
        if no_conditions > 0:
            query += ' AND '
        query += f'difficulty == \'{wordDifficulty.get()}\''
    query += f' order by oid;'
    cursor.execute(query)
    result = cursor.fetchall()
    len_results = len(result)
    if len_results == 0:
        messagebox.showwarning('No words found', 'There are no desired words in the database')
    else:
        # block buttons
        disableButtons()
        disableEntriesAndDropdown()
        # create windows with finds
        top = createFoundWordsWindow(len_results)
        Label(top, text=f'{database[:-1].upper()} words', font=("Arial", 20)).pack()
        texts = [f'{database[0].upper(), row[2]}   polish word: {row[0]}  ,  french word: {row[1]}' for row in result]
        buttons = []
        for i in range(len(texts)):
            buttons.append(Button(top, text=texts[i], font=("Arial", 14), pady=1,
                                  command=lambda i=i: selectFoundWord(top, texts[i])))
        for button in buttons:
            button.pack()

        def on_closing():
            enableButtons()
            enableEntriesAndDropdown()
            top.destroy()

        top.protocol("WM_DELETE_WINDOW", on_closing)
    connection.commit()
    connection.close()


def addTagsToQuery(no_conditions, query, tag_words):
    if no_conditions > 0:
        query += ' AND '
    if len(tag_words) > 1:
        tag_range = ', '.join(tag_words)
        query += f'(tag{1} in ({tag_range})'
        for i in range(1, len(tag_entry_list)):
            query += f' OR tag{i + 1} in ({tag_range})'
    elif len(tag_words) == 1:
        query += f'(tag{1} == {tag_words[0]}'
        for i in range(1, len(tag_entry_list)):
            query += f' OR tag{i + 1} == {tag_words[0]}'
    no_conditions += 1
    query += ')'
    return query, no_conditions


def createTagWordList():
    tag_words = []
    for i in range(len(tag_entry_list)):
        tag_value = tag_entry_list[i].get()
        if len(tag_value) > 0:
            tag_words.append(f'\'{tag_value}\'')
    return tag_words


def addWord():
    if wordCategory.get() == "all":
        messagebox.showwarning("missing data", "You NEED to select one of the available WORD CATEGORY!")
        return None
    if checkIfKeyEntriesFilled():
        database = wordCategory.get() + "s"
        connection = sqlite3.connect("french_words.db")
        cursor = connection.cursor()
        result = cursor.execute(f'select * from {database} LIMIT 1;')
        names = [description[0] for description in result.description]
        query = f"INSERT INTO {database} VALUES (:{', :'.join(names)})"
    else:
        messagebox.showwarning("missing data", "You NEED to fill POLISH AND FRENCH WORD entries!")
        return None
    if wordCategory.get() == 'basic':
        query_dictionary = {f'polish_word': polishWordEntry.get(),
                            f'french_word': frenchWordEntry.get()}
    else:
        query_dictionary = {f'polish_{wordCategory.get()}': polishWordEntry.get(),
                            f'french_{wordCategory.get()}': frenchWordEntry.get()}
    if wordCategory.get() == "noun":
        query_dictionary['french_gender'] = nounGender.get()
    elif wordCategory.get() == "verb":
        for i in range(len(verbEntryList)):
            value = verbEntryList[i].get()
            if len(value) == 0:
                query_dictionary[db_verb_list[i]] = None
            else:
                query_dictionary[db_verb_list[i]] = f'{value}'
    for i in range(len(tag_entry_list)):
        tag = tag_entry_list[i].get()
        if len(tag) == 0:
            query_dictionary[f'tag{i + 1}'] = None
        else:
            query_dictionary[f'tag{i + 1}'] = f'{tag}'
    query_dictionary['difficulty'] = f'{wordDifficulty.get()}'
    try:
        cursor.execute(query, query_dictionary)
    except sqlite3.IntegrityError:
        messagebox.showwarning("Duplicate", "There is already record of that word in this table!")
    connection.commit()
    connection.close()


def changeWord():
    # TODO: dodać powiadomienia o tym że nie ma co zmieniać, albo że zmiana rekordu się udała
    if wordCategory.get() == "all":
        messagebox.showwarning("missing data", "You NEED to select one of the available WORD CATEGORY!")
        return None
    if checkIfKeyEntriesFilled():
        database = wordCategory.get() + "s"
        start = f'UPDATE {database} SET '
    else:
        messagebox.showwarning("missing data", "You NEED to fill POLISH AND FRENCH WORD entries!")
        return None
    if wordCategory.get() == 'basic':
        end = f' WHERE polish_word = \'{polishWordEntry.get()}\' AND french_word = \'{frenchWordEntry.get()}\';'
    else:
        end = f' WHERE polish_{wordCategory.get()} = \'{polishWordEntry.get()}\' AND' \
              f' french_{wordCategory.get()} = \'{frenchWordEntry.get()}\';'
    middle_parts = []
    if wordCategory.get() == "noun":
        middle_parts.append(f'french_gender = {nounGender.get()}')
    elif wordCategory.get() == "verb":
        for i in range(len(verbEntryList)):
            value = verbEntryList[i].get()
            if len(value) == 0:
                middle_parts.append(f'{db_verb_list[i]} = NULL')
            else:
                middle_parts.append(f'{db_verb_list[i]} = \'{value}\'')
    for i in range(len(tag_entry_list)):
        tag = tag_entry_list[i].get()
        if len(tag) == 0:
            middle_parts.append(f'tag{i + 1} = NULL')
        else:
            middle_parts.append(f'tag{i + 1} = \'{tag}\'')
    middle_parts.append(f'difficulty = \'{wordDifficulty.get()}\'')
    middle = ', '.join(middle_parts)
    query = start + middle + end
    connection = sqlite3.connect("french_words.db")
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    connection.close()


def removeWord():
    if wordCategory.get() == "all":
        messagebox.showwarning("missing data", "You NEED to select one of the available WORD CATEGORY!")
        return
    if checkIfKeyEntriesFilled():
        database = wordCategory.get() + "s"
        connection = sqlite3.connect("french_words.db")
        cursor = connection.cursor()
        cursor.execute(f'select * from {database} LIMIT 1;')
        names = [description[0] for description in cursor.description]
        cursor.execute(f'DELETE FROM {database} '
                       f'WHERE {names[0]}==\'{polishWordEntry.get()}\' AND {names[1]}==\'{frenchWordEntry.get()}\';')
        clearMainScreen()
        connection.commit()
        connection.close()
        messagebox.showinfo('Success', 'Record successfuly removed from the table')
    else:
        messagebox.showwarning("missing data", "You NEED to fill POLISH AND FRENCH WORD entries!")
        return


def clearMainScreen(start=False):
    tag1.set('')
    tag2.set('')
    tag3.set('')
    polish_word.set('')
    french_word.set('')
    first_person.set('')
    second_person.set('')
    third_person.set('')
    fourth_person.set('')
    fifth_person.set('')
    sixth_person.set('')
    wordDifficulty.set("-")
    if start:
        wordCategory.set("all")
        nounGender.set("Masculine")


def enableButtons():
    for button in buttonsList:
        button['state'] = 'active'


def disableButtons():
    for button in buttonsList:
        button['state'] = 'disabled'


def enableEntriesAndDropdown():
    for entry in entriesList:
        entry.config(state='normal')
    for dropdown in dropdownsList:
        dropdown.config(state='normal')


def disableEntriesAndDropdown():
    for entry in entriesList:
        entry.config(state='disabled')
    for dropdown in dropdownsList:
        dropdown.config(state='disabled')



master = Tk()
master.title("French words database")
master.geometry("470x270")
photo = PhotoImage(file='french_flag_database.png')
master.iconphoto(True, photo)

zero_x = 10
y_jump = 20
first_x = 125
second_x = 260

wordCategoryList = ["all", "basic", "noun", "verb", "adjective"]
wordCategory = StringVar()
wordDifficulties = ["-", "easy", "normal", "hard"]
wordDifficulty = StringVar()
nounGenders = ["Masculine", "Feminine"]
nounGender = StringVar()
tag1 = StringVar()
tag2 = StringVar()
tag3 = StringVar()
polish_word = StringVar()
french_word = StringVar()
first_person = StringVar()
second_person = StringVar()
third_person = StringVar()
fourth_person = StringVar()
fifth_person = StringVar()
sixth_person = StringVar()
clearMainScreen(True)

# Labels
wordCategoryDropListLabel = Label(master, text="Word category")
wordCategoryDropListLabel.place(x=zero_x, y=55)
wordTagsLabel = Label(master, text="Tags:")
wordTagsLabel.place(x=zero_x, y=85)
polishWordLabel = Label(master, text="Polish word")
polishWordLabel.place(x=zero_x, y=110)
frenchWordLabel = Label(master, text="French word")
frenchWordLabel.place(x=zero_x, y=135)
wordDifficultyLabel = Label(master, text="Word difficulty")
wordDifficultyLabel.place(x=first_x + 100, y=55)

# Entries and list
wordCategoryDropList = OptionMenu(master, wordCategory, *wordCategoryList, command=ShowAppropriateEntries)
wordCategoryDropList.place(x=first_x, y=50)
wordDifficultyDropList = OptionMenu(master, wordDifficulty, *wordDifficulties)
wordDifficultyDropList.place(x=first_x + 200, y=50)
wordTag1Entry = Entry(master, width=18, textvariable=tag1)
wordTag1Entry.place(x=50, y=85)
wordTag2Entry = Entry(master, width=18, textvariable=tag2)
wordTag2Entry.place(x=175, y=85)
wordTag3Entry = Entry(master, width=18, textvariable=tag3)
wordTag3Entry.place(x=300, y=85)
tag_entry_list = [wordTag1Entry, wordTag2Entry, wordTag3Entry]
polishWordEntry = Entry(master, width=40, textvariable=polish_word)
polishWordEntry.place(x=first_x, y=110)
frenchWordEntry = Entry(master, width=40, textvariable=french_word)
frenchWordEntry.place(x=first_x, y=135)

# Noun spedicific labels and entries
frenchGenderLabel = Label(master, text="French noun gender")
frenchGender = OptionMenu(master, nounGender, *nounGenders)
# Verb spedicific labels and entries
db_verb_list = ['first_person', 'second_person', 'third_person',
                'fourth_person', 'fifth_person', 'sixth_person']
firstPersonLabel = Label(master, text="1st person")
firstPerson = Entry(master, width=20, textvariable=first_person)
secondPersonLabel = Label(master, text="2nd person")
secondPerson = Entry(master, width=20, textvariable=second_person)
thirdPersonLabel = Label(master, text="3rd person")
thirdPerson = Entry(master, width=20, textvariable=third_person)
fourthPersonLabel = Label(master, text="1st person")
fourthPerson = Entry(master, width=20, textvariable=fourth_person)
fifthPersonLabel = Label(master, text="2nd person")
fifthPerson = Entry(master, width=20, textvariable=fifth_person)
sixthPersonLabel = Label(master, text="3rd person")
sixthPerson = Entry(master, width=20, textvariable=sixth_person)
verbLabelsList = [firstPersonLabel, secondPersonLabel, thirdPersonLabel,
                  fourthPersonLabel, fifthPersonLabel, sixthPersonLabel]
verbEntryList = [firstPerson, secondPerson, thirdPerson, fourthPerson, fifthPerson, sixthPerson]
verbSingularLabel = Label(master, text="Singular")
verbPluralLabel = Label(master, text="Plural")

# Buttons
addWordButton = Button(master, text="Add word", width=10, pady=2,
                       command=addWord)
addWordButton.place(x=10, y=15)
button_width = 10
findWordButton = Button(master, text="Find word", width=button_width, pady=2, command=findWord)
findWordButton.place(x=100, y=15)
changeWordButton = Button(master, text="Change word", width=button_width, pady=2, command=changeWord)
changeWordButton.place(x=190, y=15)
removeWordButton = Button(master, text="Remove word", width=button_width, pady=2, command=removeWord)
removeWordButton.place(x=280, y=15)
clearEntriesButton = Button(master, text="Clear all", width=button_width, pady=2, command=clearMainScreen)
clearEntriesButton.place(x=380, y=15)

buttonsList = [addWordButton, findWordButton, changeWordButton, removeWordButton, clearEntriesButton]
entriesList = [wordTag1Entry, wordTag2Entry, wordTag3Entry, polishWordEntry, frenchWordEntry, firstPerson, secondPerson,
               thirdPerson, fourthPerson, fifthPerson, sixthPerson]
dropdownsList = [wordCategoryDropList, wordDifficultyDropList, frenchGender]

master.mainloop()
