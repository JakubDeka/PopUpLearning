from tkinter import *
import sqlite3
from tkinter import messagebox
from auxiliary import *
from pathlib import Path

project_directory = Path("D:/PythonProjects/frenchPopUp")
french_database = project_directory / "french_words.db"
image = project_directory / "images/french_flag_database.png"


def HideVerbPersons():
    for i in range(len(verbLabelsList)):
        verbLabelsList[i].place_forget()
        verbEntryList[i].place_forget()
        verbVariableList[i].set('')


def ShowAppropriateEntries(master):
    base_y = 218
    first_row_y = base_y + 25
    second_row_y = first_row_y + 25
    third_row_y = second_row_y + 25
    word_type = wordCategory.get()
    if word_type == "noun":
        # Show
        frenchGenderLabel.place(x=zero_x, y=base_y + 35)
        frenchGender.place(x=first_x, y=base_y + 30)
        # Hide
        verbSingularLabel.place_forget()
        verbPluralLabel.place_forget()
        HideVerbPersons()
    elif word_type == "verb":
        # Show
        verbSingularLabel.place(x=first_x, y=base_y)
        firstPersonLabel.place(x=zero_x, y=first_row_y)
        firstPersonEntry.place(x=first_x, y=first_row_y)
        secondPersonLabel.place(x=zero_x, y=second_row_y)
        secondPersonEntry.place(x=first_x, y=second_row_y)
        thirdPersonLabel.place(x=zero_x, y=third_row_y)
        thirdPersonEntry.place(x=first_x, y=third_row_y)
        verbPluralLabel.place(x=second_x, y=base_y)
        fourthPersonEntry.place(x=second_x, y=first_row_y)
        fifthPersonEntry.place(x=second_x, y=second_row_y)
        sixthPersonEntry.place(x=second_x, y=third_row_y)
        # Hide
        frenchGenderLabel.place_forget()
        frenchGender.place_forget()
        nounGender.set('-')
    else:
        # Hide
        frenchGenderLabel.place_forget()
        frenchGender.place_forget()
        nounGender.set('-')
        verbSingularLabel.place_forget()
        verbPluralLabel.place_forget()
        HideVerbPersons()


def checkIfPolishAndFrenchWordsFilled():
    if (len(polishWordEntry.get()) > 0) & (len(frenchWordEntry.get()) > 0):
        return True
    return False


def createFoundWordsWindow():
    top = Toplevel(master)
    top.geometry('')
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
    connection = sqlite3.connect(french_database)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {database} WHERE oid == {oid}")
    result = list(cursor.fetchmany(1)[0])
    for i in range(len(result)):
        if result[i] is None:
            result[i] = ''
    polishWord.set(result[0])
    frenchWord.set(result[1])
    tag_index = 0
    for i in range(len(tagsList), 0, -1):
        tagsList[tag_index].set(result[-i])
        tag_index += 1
    wordDifficulty.set(result[-len(tagsList) - 1])
    wordCategory.set(database[:-1])
    ShowAppropriateEntries(master)
    if database == 'nouns':
        nounGender.set(result[2])
    elif database == 'verbs':
        firstPerson.set(result[2])
        secondPerson.set(result[3])
        thirdPerson.set(result[4])
        fourthPerson.set(result[5])
        fifthPerson.set(result[6])
        sixthPerson.set(result[7])
    connection.commit()
    connection.close()
    window.destroy()


def buildQuery(function='find', target_database='basics'):
    names = findTableColumnNames(target_database)
    word_category = wordCategory.get().lower()
    database = word_category + "s"
    query_parts = []
    select_query_part = f'SELECT * FROM {database}'
    where_query_part = f' WHERE {names[0]} = \'{polishWordEntry.get().lower()}\' AND {names[1]} = ' \
                       f'\'{frenchWordEntry.get().lower()}\';'
    query_parts.append(select_query_part)
    query_parts.append(where_query_part)
    if function == 'find':
        if word_category == 'all':
            database = target_database
        find_query = f'SELECT oid, * FROM {database}'
        tag_words = createTagWordsList(tagsList)
        noun_gender = nounGender.get().lower()
        if (wordDifficulty.get() != '-') | (len(tag_words) > 0) | (len(polishWordEntry.get()) > 0) | (
                len(frenchWordEntry.get()) > 0) | (word_category == 'noun' and noun_gender != '-'):
            find_query += ' WHERE '
        no_conditions = 0
        # query condition for names
        if checkIfPolishAndFrenchWordsFilled():
            find_query += f'({names[0]}==\'{polishWordEntry.get().lower()}\' AND {names[1]}==' \
                          f'\'{frenchWordEntry.get().lower()}\')'
            no_conditions += 1
        elif (len(polishWordEntry.get()) > 0) | (len(frenchWordEntry.get()) > 0):
            find_query += f'({names[0]}==\'{polishWordEntry.get().lower()}\' OR {names[1]}==' \
                          f'\'{frenchWordEntry.get().lower()}\')'
            no_conditions += 1
        # query condition for tags
        if len(tag_words) > 0:
            find_query, no_conditions = addTagsToQuery(no_conditions, find_query, tag_words)
        if word_category == 'noun' and noun_gender != '-':
            if no_conditions > 0:
                find_query += ' AND '
            else:
                find_query += ' WHERE '
            find_query += f'french_gender == \'{noun_gender}\''
            no_conditions += 1
        if wordDifficulty.get() != '-':
            if no_conditions > 0:
                find_query += ' AND '
            find_query += f'difficulty == \'{wordDifficulty.get().lower()}\''
        find_query += f' order by oid;'
        query_parts.append(find_query)
    elif function == 'delete':
        query_parts.append(f'DELETE FROM {database}')
    elif function == 'change':
        query_parts.append(f'UPDATE {database} SET ')
    return query_parts


def packWordsFoundInTable(window, table_name, result):
    Label(window, text=f'{table_name.upper()} words', height=1, font=("Arial", 20)).pack()
    texts = [f'{table_name[0].upper(), row[0]}   PL: {row[1]}  ,  FR: {row[2]}' for row in result]
    buttons = []
    for i in range(len(texts)):
        buttons.append(Button(window, height=1, text=texts[i], font=("Arial", 14), pady=1,
                              command=lambda i=i: selectFoundWord(window, texts[i])))
    for button in buttons:
        button.pack()


def findWord():
    connection = sqlite3.connect(french_database)
    cursor = connection.cursor()
    word_category = wordCategory.get().lower()
    if word_category != 'all':
        select_query, where_query, find_query = buildQuery('find')
        print(select_query)
        cursor.execute(select_query)
        print(find_query)
        cursor.execute(find_query)
        result = [cursor.fetchall()]
        result_categories = [word_category]
        len_results = len(result[0])
        len_categories = 1
    else:
        result = []
        result_categories = []
        len_results = 0
        len_categories = 0
        for category in validWordCategories:
            select_query, where_query, find_query = buildQuery('find', category + 's')
            cursor.execute(find_query)
            temp_result = cursor.fetchall()
            temp_len = len(temp_result)
            if temp_len > 0:
                len_categories += 1
                len_results += temp_len
                result.append(temp_result)
                result_categories.append(category)
    if len_results == 0:
        messagebox.showwarning('No words found', 'There are no desired words in the database')
    else:
        # block buttons
        disableButtons()
        disableEntriesAndDropdown()
        # create windows with finds
        top = createFoundWordsWindow()
        # add title and buttons with words
        tag_words = createTagWordsList(tagsList)
        if strictTagsValue.get():
            for i in range(len_categories - 1, -1, -1):
                print(result[i])
                print(tag_words)
                restrictWordsToStrictTags(result[i], tag_words)
                print(result[i])
                if len(result[i]) == 0:
                    del result_categories[i]
                    del result[i]
                    len_categories -= 1
        for i in range(len_categories - 1, -1, -1):
            packWordsFoundInTable(top, result_categories[i], result[i])

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
    tag_range = '\', \''.join(tag_words)
    print(tag_range)
    query += f'(tag{1} in (\'{tag_range}\')'
    for i in range(1, len(tagsList)):
        query += f' OR tag{i + 1} in (\'{tag_range}\')'
    no_conditions += 1
    query += ')'
    return query, no_conditions


def findTableColumnNames(target_database='basics'):
    word_category = wordCategory.get().lower()
    if word_category != 'all':
        database = word_category + "s"
    else:
        database = target_database
    connection = sqlite3.connect(french_database)
    cursor = connection.cursor()
    cursor.execute(f'select * from {database} LIMIT 1;')
    names = [description[0] for description in cursor.description]
    connection.commit()
    connection.close()
    return names


def addWord():
    word_category = wordCategory.get().lower()
    if word_category == "all":
        messagebox.showwarning("missing data", "You NEED to select one of the available WORD CATEGORY!")
        return None
    if checkIfPolishAndFrenchWordsFilled():
        database = word_category + "s"
        connection = sqlite3.connect(french_database)
        cursor = connection.cursor()
        result = cursor.execute(f'select * from {database} LIMIT 1;')
        names = [description[0] for description in result.description]
        query = f"INSERT INTO {database} VALUES (:{', :'.join(names)})"
    else:
        messagebox.showwarning("missing data", "You NEED to fill POLISH AND FRENCH WORD entries!")
        return None
    new_polish_word = polishWordEntry.get().lower()
    new_french_word = frenchWordEntry.get().lower()
    if word_category == 'basic':
        query_dictionary = {f'polish_word': new_polish_word,
                            f'french_word': new_french_word}
    else:
        query_dictionary = {f'polish_{word_category}': new_polish_word,
                            f'french_{word_category}': new_french_word}
    if word_category == "noun":
        if nounGender.get() == '-':
            messagebox.showwarning("missing data", "You NEED to specify GENDER of the noun!")
            return
        query_dictionary['french_gender'] = nounGender.get().lower()
    elif word_category == "verb":
        for i in range(len(verbEntryList)):
            value = verbEntryList[i].get().lower()
            if len(value) == 0:
                query_dictionary[db_verb_list[i]] = None
            else:
                query_dictionary[db_verb_list[i]] = f'{value}'
    for i in range(len(tagsList)):
        tag = tagsList[i].get().lower()
        if len(tag) == 0:
            query_dictionary[f'tag{i + 1}'] = None
        else:
            query_dictionary[f'tag{i + 1}'] = f'{tag}'
    query_dictionary['difficulty'] = f'{wordDifficulty.get().lower()}'
    try:
        cursor.execute(query, query_dictionary)
        messagebox.showinfo('Success', 'Word has been added!')
        clearMainScreen()
    except sqlite3.IntegrityError:
        messagebox.showwarning("Duplicate", "There is already record of that word in this table!")
    connection.commit()
    connection.close()


def changeWord():
    word_category = wordCategory.get().lower()
    if word_category == "all":
        messagebox.showwarning("missing data", "You NEED to select one of the available WORD CATEGORY!")
        return
    if checkIfPolishAndFrenchWordsFilled():
        select_query_part, where_query_part, update_query_part = buildQuery('change')
    else:
        messagebox.showwarning("missing data", "You NEED to fill POLISH AND FRENCH WORD entries!")
        return
    find_query = select_query_part + where_query_part
    connection = sqlite3.connect(french_database)
    cursor = connection.cursor()
    cursor.execute(find_query)
    if len(cursor.execute(find_query).fetchall()) == 0:
        messagebox.showwarning('No words found', 'There are no desired words in the database')
        return
    middle_parts = []
    if word_category == "noun":
        middle_parts.append(f'french_gender = {nounGender.get().lower()}')
    elif word_category == "verb":
        for i in range(len(verbEntryList)):
            value = verbEntryList[i].get().lower()
            if len(value) == 0:
                middle_parts.append(f'{db_verb_list[i]} = NULL')
            else:
                middle_parts.append(f'{db_verb_list[i]} = \'{value}\'')
    for i in range(len(tagsList)):
        tag = tagsList[i].get().lower()
        if len(tag) == 0:
            middle_parts.append(f'tag{i + 1} = NULL')
        else:
            middle_parts.append(f'tag{i + 1} = \'{tag}\'')
    middle_parts.append(f'difficulty = \'{wordDifficulty.get().lower()}\'')
    middle = ', '.join(middle_parts)
    update_query = update_query_part + middle + where_query_part
    cursor.execute(update_query)
    connection.commit()
    connection.close()
    messagebox.showinfo('Success', 'Record successfully changed')


def removeWord():
    if wordCategory.get().lower() == "all":
        messagebox.showwarning("missing data", "You NEED to select one of the available WORD CATEGORY!")
        return
    if checkIfPolishAndFrenchWordsFilled():
        select_query_part, where_query_part, delete_query = buildQuery('delete')
        connection = sqlite3.connect(french_database)
        cursor = connection.cursor()
        if len(cursor.execute(select_query_part + where_query_part).fetchall()) == 0:
            messagebox.showwarning('No words found', 'There are no desired words in the database')
            return
        cursor.execute(delete_query + where_query_part)
        connection.commit()
        connection.close()
        clearMainScreen()
        messagebox.showinfo('Success', 'Record successfully removed from the table')
    else:
        messagebox.showwarning("missing data", "You NEED to fill POLISH AND FRENCH WORD entries!")
        return


def clearMainScreen(start=False):
    for tag in tagsList:
        tag.set('')
    polishWord.set('')
    frenchWord.set('')
    for person in personsList:
        person.set('')
    wordDifficulty.set("-")
    if start:
        wordCategory.set("all")
        nounGender.set("-")


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
    strictTagsCheckbox.config(state='normal')


def disableEntriesAndDropdown():
    for entry in entriesList:
        entry.config(state='disabled')
    for dropdown in dropdownsList:
        dropdown.config(state='disabled')
    strictTagsCheckbox.config(state='disabled')


master = Tk()
master.title("French words database")
master.geometry("490x325")
photo = PhotoImage(file=image)
master.iconphoto(True, photo)

zero_x = 10
y_jump = 20
first_x = 125
second_x = 260

wordCategoryList = ["all", "basic", "noun", "verb", "adjective"]
validWordCategories = ["basic", "noun", "verb", "adjective"]
wordCategory = StringVar()
wordDifficulties = ["-", "easy", "normal", "hard"]
wordDifficulty = StringVar()
nounGenders = ['-', "masculine", "feminine"]
nounGender = StringVar()
tag1 = StringVar()
tag2 = StringVar()
tag3 = StringVar()
tag4 = StringVar()
tag5 = StringVar()
tag6 = StringVar()
tagsList = [tag1, tag2, tag3, tag4, tag5, tag6]
polishWord = StringVar()
frenchWord = StringVar()
firstPerson = StringVar()
secondPerson = StringVar()
thirdPerson = StringVar()
fourthPerson = StringVar()
fifthPerson = StringVar()
sixthPerson = StringVar()
personsList = [firstPerson, secondPerson, thirdPerson, fourthPerson, fifthPerson, sixthPerson]
clearMainScreen(True)

# Labels
tags_y = 170

wordCategoryDropListLabel = Label(master, text="Word category")
wordCategoryDropListLabel.place(x=zero_x, y=55)
wordTagsLabel = Label(master, text="Tags:")
wordTagsLabel.place(x=zero_x, y=tags_y)
polishWordLabel = Label(master, text="Polish word")
polishWordLabel.place(x=zero_x, y=tags_y - 75)
frenchWordLabel = Label(master, text="French word")
frenchWordLabel.place(x=zero_x, y=tags_y - 50)
wordDifficultyLabel = Label(master, text="Word difficulty")
wordDifficultyLabel.place(x=first_x + 90, y=55)

# Entries and list
wordCategoryDropList = OptionMenu(master, wordCategory, *wordCategoryList, command=ShowAppropriateEntries)
wordCategoryDropList.place(x=first_x - 31, y=50)
wordDifficultyDropList = OptionMenu(master, wordDifficulty, *wordDifficulties)
wordDifficultyDropList.place(x=first_x + 180, y=50)
wordTag1Entry = Entry(master, width=20, textvariable=tag1)
wordTag1Entry.place(x=50, y=tags_y)
wordTag2Entry = Entry(master, width=20, textvariable=tag2)
wordTag2Entry.place(x=185, y=tags_y)
wordTag3Entry = Entry(master, width=20, textvariable=tag3)
wordTag3Entry.place(x=320, y=tags_y)
wordTag4Entry = Entry(master, width=20, textvariable=tag4)
wordTag4Entry.place(x=50, y=tags_y + 25)
wordTag5Entry = Entry(master, width=20, textvariable=tag5)
wordTag5Entry.place(x=185, y=tags_y + 25)
wordTag6Entry = Entry(master, width=20, textvariable=tag6)
wordTag6Entry.place(x=320, y=tags_y + 25)
tagEntryList = [wordTag1Entry, wordTag2Entry, wordTag3Entry, wordTag4Entry, wordTag5Entry, wordTag6Entry]
polishWordEntry = Entry(master, width=40, textvariable=polishWord)
polishWordEntry.place(x=first_x, y=tags_y - 75)
frenchWordEntry = Entry(master, width=40, textvariable=frenchWord)
frenchWordEntry.place(x=first_x, y=tags_y - 50)

# tag specific checkbox
strictTagsValue = IntVar()
strictTagsCheckbox = Checkbutton(master, text='Strict tags', variable=strictTagsValue)
strictTagsCheckbox.place(x=10, y=tags_y - 25)

# Noun spedicific labels and entries
frenchGenderLabel = Label(master, text="French noun gender")
frenchGender = OptionMenu(master, nounGender, *nounGenders)
# Verb spedicific labels and entries
db_verb_list = ['first_person', 'second_person', 'third_person',
                'fourth_person', 'fifth_person', 'sixth_person']
firstPersonLabel = Label(master, text="1st person")
firstPersonEntry = Entry(master, width=20, textvariable=firstPerson)
secondPersonLabel = Label(master, text="2nd person")
secondPersonEntry = Entry(master, width=20, textvariable=secondPerson)
thirdPersonLabel = Label(master, text="3rd person")
thirdPersonEntry = Entry(master, width=20, textvariable=thirdPerson)
fourthPersonLabel = Label(master, text="1st person")
fourthPersonEntry = Entry(master, width=20, textvariable=fourthPerson)
fifthPersonLabel = Label(master, text="2nd person")
fifthPersonEntry = Entry(master, width=20, textvariable=fifthPerson)
sixthPersonLabel = Label(master, text="3rd person")
sixthPersonEntry = Entry(master, width=20, textvariable=sixthPerson)
verbLabelsList = [firstPersonLabel, secondPersonLabel, thirdPersonLabel,
                  fourthPersonLabel, fifthPersonLabel, sixthPersonLabel]
verbEntryList = [firstPersonEntry, secondPersonEntry, thirdPersonEntry,
                 fourthPersonEntry, fifthPersonEntry, sixthPersonEntry]
verbVariableList = [firstPerson, secondPerson, thirdPerson, fourthPerson, fifthPerson, sixthPerson]
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
clearEntriesButton.place(x=395, y=15)

buttonsList = [addWordButton, findWordButton, changeWordButton, removeWordButton, clearEntriesButton]
entriesList = [polishWordEntry, frenchWordEntry, firstPersonEntry, secondPersonEntry,
               thirdPersonEntry, fourthPersonEntry, fifthPersonEntry, sixthPersonEntry,
               wordTag1Entry, wordTag2Entry, wordTag3Entry, wordTag4Entry, wordTag5Entry, wordTag6Entry]
dropdownsList = [wordCategoryDropList, wordDifficultyDropList, frenchGender]

master.mainloop()
