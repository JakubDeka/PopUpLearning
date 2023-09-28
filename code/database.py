from tkinter import *
from tkinter import messagebox
from auxiliary import *
from ttkwidgets.autocomplete import AutocompleteEntry


project_directory, french_database = loadDirectories()
image = project_directory / "images/french_flag_database.png"


def HideVerbPersons():
    for i in range(len(verbLabelsList)):
        verbLabelsList[i].grid_forget()
        verbEntryList[i].grid_forget()
        verbVariableList[i].set('')


def ShowAppropriateEntries(master_window):
    word_type = getEnglishWordCategory()
    if word_type == "noun":
        # Show
        categorySpecificFrame.grid(row=4, column=1, columnspan=2, sticky=E + W, pady=frameAwayFromBorderY / 2)
        frenchGenderLabel.grid(row=0, column=0)
        frenchGender.grid(row=0, column=1)
        frenchGender.config(width=10)
        # Hide
        verbSingularLabel.grid_forget()
        verbPluralLabel.grid_forget()
        HideVerbPersons()
    elif word_type == "verb":
        # Show
        categorySpecificFrame.grid(row=4, column=1, sticky=E + W, pady=frameAwayFromBorderY / 2)
        verbSingularLabel.grid(row=0, column=1)
        firstPersonLabel.grid(row=1, column=0)
        firstPersonEntry.grid(row=1, column=1, padx=15, pady=2)
        secondPersonLabel.grid(row=2, column=0)
        secondPersonEntry.grid(row=2, column=1, padx=15, pady=2)
        thirdPersonLabel.grid(row=3, column=0)
        thirdPersonEntry.grid(row=3, column=1, padx=15, pady=2)
        verbPluralLabel.grid(row=0, column=2)
        fourthPersonEntry.grid(row=1, column=2)
        fifthPersonEntry.grid(row=2, column=2)
        sixthPersonEntry.grid(row=3, column=2)
        # Hide
        frenchGenderLabel.grid_forget()
        frenchGender.grid_forget()
        nounGender.set('-')
    else:
        # Hide
        frenchGenderLabel.grid_forget()
        frenchGender.grid_forget()
        nounGender.set('-')
        verbSingularLabel.grid_forget()
        verbPluralLabel.grid_forget()
        categorySpecificFrame.grid_forget()
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
    connection = sqlite3.connect(frenchDatabase)
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
    wordDifficulty.set(english_polish_dictionary[result[-len(tagsList) - 1]])
    wordCategory.set(english_polish_dictionary[database[:-1]])
    ShowAppropriateEntries(master)
    if database == 'nouns':
        nounGender.set(english_polish_dictionary[result[2]])
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


def getEnglishWordCategory():
    word_category = wordCategory.get().lower()
    if word_category in polishWordCategoryList:
        word_category = polish_english_dictionary[word_category]
    return word_category


def getEnglishWordDifficulty():
    word_difficulty = wordCategory.get().lower()
    if word_difficulty in polishWordDifficultyList:
        word_difficulty = polish_english_dictionary[word_difficulty]
    return word_difficulty


def getEnglishNounGender():
    noun_gender = nounGender.get().lower()
    if noun_gender in polishNounGenderList:
        noun_gender = polish_english_dictionary[noun_gender]
    return noun_gender


def buildQuery(function='find', target_database='basics'):
    names = findTableColumnNames(target_database)
    word_category = getEnglishWordCategory()
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
            find_query += f'french_gender == \'{getEnglishNounGender()}\''
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
    for j in range(len(texts)):
        buttons.append(Button(window, height=1, text=texts[j], font=("Arial", 14), width=40, pady=1,
                              command=lambda i=j: selectFoundWord(window, texts[i])))
    for button in buttons:
        button.pack()


def findWord():
    connection = sqlite3.connect(frenchDatabase)
    cursor = connection.cursor()
    word_category = getEnglishWordCategory()
    if word_category != 'all':
        select_query, where_query, find_query = buildQuery('find')
        cursor.execute(select_query)
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
        for category in validWordCategoryList:
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
                restrictWordsToStrictTags(result[i], tag_words)
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
    query += f'(tag{1} in (\'{tag_range}\')'
    for i in range(1, len(tagsList)):
        query += f' OR tag{i + 1} in (\'{tag_range}\')'
    no_conditions += 1
    query += ')'
    return query, no_conditions


def findTableColumnNames(target_database='basics'):
    word_category = getEnglishWordCategory()
    if word_category != 'all':
        database = word_category + "s"
    else:
        database = target_database
    connection = sqlite3.connect(frenchDatabase)
    cursor = connection.cursor()
    cursor.execute(f'select * from {database} LIMIT 1;')
    names = [description[0] for description in cursor.description]
    connection.commit()
    connection.close()
    return names


def addWord():
    global availableLabels
    word_category = getEnglishWordCategory()
    if word_category == "all":
        messagebox.showwarning("missing data", "You NEED to select one of the available WORD CATEGORY!")
        return None
    if checkIfPolishAndFrenchWordsFilled():
        database = word_category + "s"
        connection = sqlite3.connect(frenchDatabase)
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
            verb_value = verbEntryList[i].get().lower()
            if len(verb_value) == 0:
                query_dictionary[db_verb_list[i]] = None
            else:
                query_dictionary[db_verb_list[i]] = f'{verb_value}'
    word_tags_list = []
    for i in range(len(tagsList)):
        tag = tagsList[i].get().lower()
        word_tags_list.append(tag)
        if len(tag) == 0:
            query_dictionary[f'tag{i + 1}'] = None
        else:
            query_dictionary[f'tag{i + 1}'] = f'{tag}'
    query_dictionary['difficulty'] = f'{wordDifficulty.get().lower()}'
    try:
        cursor.execute(query, query_dictionary)
        messagebox.showinfo('Success', 'Word has been added!')
        availableLabels += word_tags_list
        availableLabels = uniqueValuesInListLike(availableLabels)
        clearMainScreen()
    except sqlite3.IntegrityError:
        messagebox.showwarning("Duplicate", "There is already record of that word in this table!")
    connection.commit()
    connection.close()


def changeWord():
    word_category = getEnglishWordCategory()
    if word_category == "all":
        messagebox.showwarning("missing data", "You NEED to select one of the available WORD CATEGORY!")
        return
    if checkIfPolishAndFrenchWordsFilled():
        select_query_part, where_query_part, update_query_part = buildQuery('change')
    else:
        messagebox.showwarning("missing data", "You NEED to fill POLISH AND FRENCH WORD entries!")
        return
    find_query = select_query_part + where_query_part
    connection = sqlite3.connect(frenchDatabase)
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
        connection = sqlite3.connect(frenchDatabase)
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
        wordCategory.set("wszystko")
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


def adjustToLanguage():
    if language.get() == 'english':
        mainFrameWidthModifier.set(1)
        labelFramePadX.set(111)
        # changeLanguageButton.place_forget()
        # changeLanguageButton.place(x=430, y=5)
        appMainLabelText.set('Tool for words management')
        changeLanguageText.set('Change language')
        categoryLabelText.set('Word category')
        polishWordLabelText1.set('Polish word')
        frenchWordLabelText1.set('French word')
        wordDifficultyLabelText1.set('Word difficulty')
        tagsLabelText.set('Tags')
        strictTagsLabelText.set('Strict tags')
        frenchNounGenderLabelText.set('French noun gender')
        firstPersonLabelText.set('1st person')
        secondPersonLabelText.set('2nd person')
        thirdPersonLabelText.set('3rd person')
        singularLabelText.set('Singular')
        pluralLabelText.set('Plural')
        addLabelText.set('Add')
        findLabelText.set('Find')
        modifyLabelText.set('Modify')
        deleteLabelText.set('Delete')
        clearAllLabelText.set('Clear all')
        how_many_gender_button_times.set(2)
    else:
        mainFrameWidthModifier.set(0.8)
        labelFramePadX.set(22)
        how_many_gender_button_times.set(4)
        # changeLanguageButton.place_forget()
        # changeLanguageButton.place(x=450, y=5)
        categoryLabelText.set('Kategoria słowa')
        polishWordLabelText1.set('Polskie słowo')
        frenchWordLabelText1.set('Francuskie słowo')
        wordDifficultyLabelText1.set('Trudność słowa')
        tagsLabelText.set('Tagi')
        strictTagsLabelText.set('Dokładne tagi')
        frenchNounGenderLabelText.set('Płeć francuskiego rzeczownika')
        firstPersonLabelText.set('1st osoba')
        secondPersonLabelText.set('2nd osoba')
        thirdPersonLabelText.set('3rd osoba')
        singularLabelText.set('L. pojedyncza')
        pluralLabelText.set('L. mnoga')
        addLabelText.set('Dodaj')
        findLabelText.set('Znajdź')
        modifyLabelText.set('Modyfikuj')
        deleteLabelText.set('Usuń')
        clearAllLabelText.set('Wyczyść')
        appMainLabelText.set('Narzędzie do zarządzania słowami')
        changeLanguageText.set('Zmień język')


def changeLanguage():
    if language.get() == 'english':
        language.set('polish')
    else:
        language.set('english')
    adjustToLanguage()


def openMenu():
    master.destroy()


master = Tk()
master.title("French words database")
frameAwayFromBorderY = 10
master.config(bg='#D2DEE6')
photo = PhotoImage(file=image)
master.iconphoto(True, photo)

how_many_gender_button_times = IntVar()
language = StringVar()
language.set('polish')
wordCategoryList = ['all', 'basic', 'noun', 'verb', 'adjective']
polishWordCategoryList = ['wszystko', 'podstawowe', 'rzeczownik', 'czasownik', 'przymiotnik']
validWordCategoryList = ['basic', 'noun', 'verb', 'adjective']
wordCategory = StringVar()
wordDifficultyList = ['-', 'easy', 'medium', 'hard']
polishWordDifficultyList = ['-', 'łatwy', 'średni', 'trudny']
wordDifficulty = StringVar()
nounGenderList = ['-', 'masculine', 'feminine']
polishNounGenderList = ['-', 'męska', 'żeńska']
nounGender = StringVar()

english_polish_dictionary, polish_english_dictionary, allList, basicList, verbList, nounList, adjectiveList =\
    generateDictionariesAndLanLists()

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

appMainLabelText = StringVar()
changeLanguageText = StringVar()
categoryLabelText = StringVar()
polishWordLabelText1 = StringVar()
frenchWordLabelText1 = StringVar()
wordDifficultyLabelText1 = StringVar()
tagsLabelText = StringVar()
strictTagsLabelText = StringVar()
frenchNounGenderLabelText = StringVar()
firstPersonLabelText = StringVar()
secondPersonLabelText = StringVar()
thirdPersonLabelText = StringVar()
singularLabelText = StringVar()
pluralLabelText = StringVar()
addLabelText = StringVar()
findLabelText = StringVar()
modifyLabelText = StringVar()
deleteLabelText = StringVar()
clearAllLabelText = StringVar()
labelTextsList = [categoryLabelText, polishWordLabelText1, frenchWordLabelText1, wordDifficultyLabelText1,
                  tagsLabelText,
                  strictTagsLabelText, frenchNounGenderLabelText, firstPersonLabelText, secondPersonLabelText,
                  thirdPersonLabelText, singularLabelText, pluralLabelText, addLabelText, findLabelText,
                  modifyLabelText, deleteLabelText, clearAllLabelText, appMainLabelText, changeLanguageText]
mainFrameWidthModifier = DoubleVar()
labelFramePadX = IntVar()
# only one lang version uses that
labelFramePadX.set(22)
mainFrameWidthModifier.set(0.8)

# App label
Label(master, textvariable=appMainLabelText, font=("Arial", 20), bg='#D2DEE6').grid(row=0, column=1, ipadx=10, ipady=5)
Label(master, text='', font=("Arial", 20), bg='#D2DEE6').grid(row=0, column=0, ipadx=10, ipady=5)
Label(master, text='', font=("Arial", 20), bg='#D2DEE6').grid(row=0, column=3, ipadx=10, ipady=5)
# changeLanguageButton = Button(master, textvariable=changeLanguageText, command=changeLanguage)
# changeLanguageButton.place(x=450, y=5)

# Main frame
mainFrame = LabelFrame(master, padx=30, pady=2)
mainFrame.grid(row=2, column=1, columnspan=2, ipady=5, sticky=E + W, pady=frameAwayFromBorderY)
# Main frame
wordEntryWidth = 60
wordEntrySpan = 4
wordCategoryDropListLabel = Label(mainFrame, textvariable=categoryLabelText, pady=8)
wordCategoryDropListLabel.grid(row=0, column=0)
wordCategoryDropList = OptionMenu(mainFrame, wordCategory, *polishWordCategoryList, command=ShowAppropriateEntries)
wordCategoryDropList.grid(row=0, column=1, ipadx=12)
wordCategoryDropList.config(width=7)

polishWordLabelText = Label(mainFrame, textvariable=polishWordLabelText1, pady=3)
polishWordLabelText.grid(row=1, column=0)
polishWordEntry = Entry(mainFrame, width=wordEntryWidth, textvariable=polishWord)
polishWordEntry.grid(row=1, columnspan=wordEntrySpan, column=1)
frenchWordLabelText = Label(mainFrame, textvariable=frenchWordLabelText1, pady=6)
frenchWordLabelText.grid(row=2, column=0)
frenchWordEntry = Entry(mainFrame, width=wordEntryWidth, textvariable=frenchWord)
frenchWordEntry.grid(row=2, columnspan=wordEntrySpan, column=1)

wordDifficultyLabelText = Label(mainFrame, textvariable=wordDifficultyLabelText1, pady=8)
wordDifficultyLabelText.grid(row=0, column=3)
wordDifficultyDropList = OptionMenu(mainFrame, wordDifficulty, *polishWordDifficultyList)
wordDifficultyDropList.grid(row=0, column=4, ipadx=12)
wordDifficultyDropList.config(width=7)

availableLabels = createAvailableLabelsList(validWordCategoryList, tagsList)
availableLabels.remove(None)

# Labels frame
tagEntryWidth = 22
labelsFrame = LabelFrame(master, padx=labelFramePadX.get(), pady=2, bg='#EBEBD2')
labelsFrame.grid(row=3, column=1, columnspan=2, ipadx=10, ipady=5, sticky=E + W, pady=frameAwayFromBorderY / 2)
wordTagsLabel = Label(labelsFrame, textvariable=tagsLabelText, bg='#EBEBD2')
wordTagsLabel.grid(row=0, column=0)
wordTag1Entry = AutocompleteEntry(labelsFrame, width=tagEntryWidth, textvariable=tag1, completevalues=availableLabels)
wordTag1Entry.grid(row=0, column=1, padx=3, pady=3)
wordTag2Entry = AutocompleteEntry(labelsFrame, width=tagEntryWidth, textvariable=tag2, completevalues=availableLabels)
wordTag2Entry.grid(row=0, column=2, padx=3, pady=3)
wordTag3Entry = AutocompleteEntry(labelsFrame, width=tagEntryWidth, textvariable=tag3, completevalues=availableLabels)
wordTag3Entry.grid(row=0, column=3, padx=3, pady=3)
wordTag4Entry = AutocompleteEntry(labelsFrame, width=tagEntryWidth, textvariable=tag4, completevalues=availableLabels)
wordTag4Entry.grid(row=1, column=1, padx=3, pady=3)
wordTag5Entry = AutocompleteEntry(labelsFrame, width=tagEntryWidth, textvariable=tag5, completevalues=availableLabels)
wordTag5Entry.grid(row=1, column=2, padx=3, pady=3)
wordTag6Entry = AutocompleteEntry(labelsFrame, width=tagEntryWidth, textvariable=tag6, completevalues=availableLabels)
wordTag6Entry.grid(row=1, column=3, padx=3, pady=3)

# tag specific checkbox
strictTagsValue = IntVar()
strictTagsCheckbox = Checkbutton(labelsFrame, textvariable=strictTagsLabelText, variable=strictTagsValue, bg='#EBEBD2')
strictTagsCheckbox.grid(row=2, column=1)

# Category specific frame
categorySpecificFrame = LabelFrame(master, padx=labelFramePadX.get(), pady=2, bg='#F0D3AC')

# Noun spedicific labels and entries
frenchGenderLabel = Label(categorySpecificFrame, textvariable=frenchNounGenderLabelText, bg='#F0D3AC')
frenchGender = OptionMenu(categorySpecificFrame, nounGender, *polishNounGenderList)
# Verb spedicific labels and entries
db_verb_list = ['first_person', 'second_person', 'third_person',
                'fourth_person', 'fifth_person', 'sixth_person']
personEntryWidth = 25
firstPersonLabel = Label(categorySpecificFrame, textvariable=firstPersonLabelText, bg='#F0D3AC')
firstPersonEntry = Entry(categorySpecificFrame, width=personEntryWidth, textvariable=firstPerson)
secondPersonLabel = Label(categorySpecificFrame, textvariable=secondPersonLabelText, bg='#F0D3AC')
secondPersonEntry = Entry(categorySpecificFrame, width=personEntryWidth, textvariable=secondPerson)
thirdPersonLabel = Label(categorySpecificFrame, textvariable=thirdPersonLabelText, bg='#F0D3AC')
thirdPersonEntry = Entry(categorySpecificFrame, width=personEntryWidth, textvariable=thirdPerson)
fourthPersonLabel = Label(categorySpecificFrame, textvariable=firstPersonLabelText)
fourthPersonEntry = Entry(categorySpecificFrame, width=personEntryWidth, textvariable=fourthPerson)
fifthPersonLabel = Label(categorySpecificFrame, textvariable=firstPersonLabelText)
fifthPersonEntry = Entry(categorySpecificFrame, width=personEntryWidth, textvariable=fifthPerson)
sixthPersonLabel = Label(categorySpecificFrame, textvariable=firstPersonLabelText)
sixthPersonEntry = Entry(categorySpecificFrame, width=personEntryWidth, textvariable=sixthPerson)
verbLabelsList = [firstPersonLabel, secondPersonLabel, thirdPersonLabel,
                  fourthPersonLabel, fifthPersonLabel, sixthPersonLabel]
verbEntryList = [firstPersonEntry, secondPersonEntry, thirdPersonEntry,
                 fourthPersonEntry, fifthPersonEntry, sixthPersonEntry]
verbVariableList = [firstPerson, secondPerson, thirdPerson, fourthPerson, fifthPerson, sixthPerson]
verbSingularLabel = Label(categorySpecificFrame, textvariable=singularLabelText, bg='#F0D3AC')
verbPluralLabel = Label(categorySpecificFrame, textvariable=pluralLabelText, bg='#F0D3AC')

# Buttons frame
buttonsFrame = LabelFrame(master, padx=frameAwayFromBorderY / 2, pady=2, bg='#A6AEB3')
buttonsFrame.grid(row=1, column=1, columnspan=2, ipadx=10, ipady=5, sticky=E + W)
button_width = 10
button_pad_y = 5
buttonsColors = ['#2BA531', '#046791', '#5D5B39', '#96465A', '#5455CD']
addWordButton = Button(buttonsFrame, textvariable=addLabelText, width=button_width, pady=button_pad_y,
                       command=addWord, bg='#2BA531')
addWordButton.grid(row=0, column=0, pady=10, padx=10)
findWordButton = Button(buttonsFrame, textvariable=findLabelText, width=button_width, pady=button_pad_y,
                        command=findWord,
                        bg='#046791')
findWordButton.grid(row=0, column=1, pady=10, padx=10)
changeWordButton = Button(buttonsFrame, textvariable=modifyLabelText, width=button_width, pady=button_pad_y,
                          command=changeWord,
                          bg='#5D5B39')
changeWordButton.grid(row=0, column=2, pady=10, padx=10)
removeWordButton = Button(buttonsFrame, textvariable=deleteLabelText, width=button_width, pady=button_pad_y,
                          command=removeWord,
                          bg='#96465A')
removeWordButton.grid(row=0, column=3, pady=10, padx=10)
clearEntriesButton = Button(buttonsFrame, textvariable=clearAllLabelText, width=button_width, pady=button_pad_y,
                            command=clearMainScreen, bg='#5455CD')
clearEntriesButton.grid(row=0, column=4, pady=10, padx=10)
menuButton = Button(master, text="MENU", width=12, pady=2, command=openMenu, bg='#C5D2EC')
menuButton.grid(row=0, column=2)

buttonsList = [addWordButton, findWordButton, changeWordButton, removeWordButton, clearEntriesButton, menuButton]
entriesList = [polishWordEntry, frenchWordEntry, firstPersonEntry, secondPersonEntry,
               thirdPersonEntry, fourthPersonEntry, fifthPersonEntry, sixthPersonEntry,
               wordTag1Entry, wordTag2Entry, wordTag3Entry, wordTag4Entry, wordTag5Entry, wordTag6Entry]
dropdownsList = [wordCategoryDropList, wordDifficultyDropList, frenchGender]

# master.geometry(f"680x200")
clearMainScreen(True)
adjustToLanguage()
master.resizable(width=False, height=False)
master.mainloop()
