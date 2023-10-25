from auxiliary import *
from generate_database_elements import *
from ttkwidgets.autocomplete import AutocompleteEntry

normal_symbols, strange_symbols = generateNormalAndStrangeSymbolDicts()


def HideVerbPersons():
    for i in range(len(verbLabelsList)):
        verbLabelsList[i].grid_forget()
        verbEntryList[i].grid_forget()
        verbVariableList[i].set('')


def ShowAppropriateEntries(master_window):
    word_type = getEnglishWordCategory()
    if word_type == "noun" and taughtLanguage == 'french':
        # Show
        categorySpecificFrame.grid(row=4, column=1, columnspan=2, sticky=E + W, pady=frameAwayFromBorderY / 2)
        foreignGenderLabel.grid(row=0, column=0)
        foreignGender.grid(row=0, column=1)
        foreignGender.config(width=10)
        # Hide
        verbSingularLabel.grid_forget()
        verbPluralLabel.grid_forget()
        HideVerbPersons()
    elif word_type == "verb":
        # Show
        if taughtLanguage == 'french':
            categorySpecificFrame.grid(row=4, column=1, sticky=E + W, pady=frameAwayFromBorderY / 2)
            verbSingularLabel.grid(row=0, column=1)
            verbPluralLabel.grid(row=0, column=2)
            firstPersonLabel.grid(row=1, column=0)
            firstPersonEntry.grid(row=1, column=1, padx=15, pady=2)
            secondPersonLabel.grid(row=2, column=0)
            secondPersonEntry.grid(row=2, column=1, padx=15, pady=2)
            thirdPersonLabel.grid(row=3, column=0)
            thirdPersonEntry.grid(row=3, column=1, padx=15, pady=2)
            fourthPersonEntry.grid(row=1, column=2)
            fifthPersonEntry.grid(row=2, column=2)
            sixthPersonEntry.grid(row=3, column=2)
            # Hide
            foreignGenderLabel.grid_forget()
            foreignGender.grid_forget()
            nounGender.set('-')
        elif taughtLanguage == 'english':
            categorySpecificFrame.grid(row=4, column=1, columnspan=2, sticky=E + W, pady=frameAwayFromBorderY / 2)
            firstPersonLabel.grid(row=1, column=0)
            firstPersonEntry.grid(row=2, column=0, padx=3, pady=2)
            secondPersonLabel.grid(row=1, column=1)
            secondPersonEntry.grid(row=2, column=1, padx=3, pady=2)
            thirdPersonLabel.grid(row=1, column=2)
            thirdPersonEntry.grid(row=2, column=2, padx=3, pady=2)

    else:
        # Hide
        if taughtLanguage == 'french':
            foreignGenderLabel.grid_forget()
            foreignGender.grid_forget()
            nounGender.set('-')
        verbSingularLabel.grid_forget()
        verbPluralLabel.grid_forget()
        categorySpecificFrame.grid_forget()
        HideVerbPersons()


def checkIfPolishAndForeignWordsFilled():
    if (len(getPolishWord()) > 0) & (len(getForeignWord()) > 0):
        return True
    return False


def createFoundWordsWindow():
    top = Toplevel(master)
    top.geometry('')
    top.title("Found words")
    return top


def selectFoundWord(window_to_close, text):
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
    connection = sqlite3.connect(foreignDatabase)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {database} WHERE oid == {oid}")
    result = list(cursor.fetchmany(1)[0])
    for i in range(len(result)):
        if result[i] is None:
            result[i] = ''
    polishWord.set(replaceSymbolsInString(result[0], strange_symbols))
    foreignWord.set(replaceSymbolsInString(result[1], strange_symbols))
    tag_index = 0
    for i in range(len(tagsValueList), 0, -1):
        tagsValueList[tag_index].set(replaceSymbolsInString(result[-i], strange_symbols))
        tag_index += 1
    if guiLanguage.get() == 'polish':
        wordDifficulty.set(english_polish_dictionary[result[-len(tagsValueList) - 1]])
        wordCategory.set(english_polish_dictionary[database[:-1]])
    else:
        wordDifficulty.set(result[-len(tagsValueList) - 1])
        wordCategory.set(database[:-1])
    ShowAppropriateEntries(master)
    if database == 'nouns' and taughtLanguage == 'french':
        nounGender.set(english_polish_dictionary[result[2]])
    elif database == 'verbs':
        i = 2
        for person_value in personsList:
            person_value.set(replaceSymbolsInString(result[i], strange_symbols))
            i += 1
    connection.commit()
    connection.close()
    availableTagsList.set('')
    polishWordEntry.focus()
    window_to_close.destroy()


def getEnglishWordCategory():
    word_category = wordCategory.get().lower()
    if word_category in polishWordCategoryList:
        word_category = polish_english_dictionary[word_category]
    return word_category


def getEnglishNounGender():
    noun_gender = nounGender.get().lower()
    if noun_gender in polishNounGenderList:
        noun_gender = polish_english_dictionary[noun_gender]
    return noun_gender


def getEnglishDifficulty():
    difficulty = wordDifficulty.get().lower()
    if difficulty in polishWordDifficultyList:
        difficulty = polish_english_dictionary[difficulty]
    return difficulty


def getPolishWord():
    polish_word = polishWordEntry.get().lower().strip()
    return replaceSymbolsInString(polish_word, normal_symbols)


def getForeignWord():
    foreign_word = foreignWordEntry.get().lower().strip()
    return replaceSymbolsInString(foreign_word, normal_symbols)


def buildQuery(function='find', target_database='basics'):
    names = findTableColumnNames(target_database)
    word_category = getEnglishWordCategory()
    database = word_category + "s"
    query_parts = []
    select_query_part = f'SELECT * FROM {database}'
    where_query_part = f' WHERE {names[0]} = \'{getPolishWord()}\' AND {names[1]} = \'{getForeignWord()}\';'
    query_parts.append(select_query_part)
    query_parts.append(where_query_part)
    if function == 'find':
        if word_category == 'all':
            database = target_database
        find_query = f'SELECT oid, * FROM {database}'
        tag_words = createTagWordsList(tagsValueList, normal_symbols)
        noun_gender = getEnglishNounGender()
        if (wordDifficulty.get() != '-') | (len(tag_words) > 0) | (len(getPolishWord()) > 0) | (
                len(getForeignWord()) > 0) | (word_category == 'noun' and noun_gender != '-'):
            find_query += ' WHERE '
        no_conditions = 0
        # query condition for names
        if checkIfPolishAndForeignWordsFilled():
            find_query += f'({names[0]}==\'{getPolishWord()}\' AND {names[1]}==\'{getForeignWord()}\')'
            no_conditions += 1
        elif (len(getPolishWord()) > 0) | (len(getForeignWord()) > 0):
            find_query += f'({names[0]}==\'{getPolishWord()}\' OR {names[1]}==\'{getForeignWord()}\')'
            no_conditions += 1
        # query condition for tags
        if len(tag_words) > 0:
            find_query, no_conditions = addTagsToQuery(no_conditions, find_query, tag_words)
        if word_category == 'noun' and taughtLanguage == 'french' and noun_gender != '-':
            if no_conditions > 0:
                find_query += ' AND '
            find_query += f'{taughtLanguage}_gender == \'{getEnglishNounGender()}\''
            no_conditions += 1
        if wordDifficulty.get() != '-':
            if no_conditions > 0:
                find_query += ' AND '
            find_query += f'difficulty == \'{getEnglishDifficulty():}\''
        find_query += f' order by oid;'
        query_parts.append(find_query)
    elif function == 'delete':
        query_parts.append(f'DELETE FROM {database}')
    elif function == 'change':
        query_parts.append(f'UPDATE {database} SET ')
    return query_parts


def packWordsFoundInTable(window, window_to_close, table_name, result):
    text = table_name.upper() + 'S'
    if guiLanguage.get() == 'polish':
        text = english_polish_dictionary[table_name].upper() + 'I'
    if table_name in ['basic']:
        text = text[:-1]
    Label(window, text=text, height=1, font=("Arial", 20)).pack()
    texts = []
    for row in result:
        db_string = f'{table_name[0].upper(), row[0]}'
        db_padding = 10 - len(db_string)
        pl_string = f'PL: {replaceSymbolsInString(row[1], strange_symbols)}'
        pl_padding = 25 - len(pl_string)
        fl_string = f'FR: {replaceSymbolsInString(row[2], strange_symbols)}'
        fl_padding = 25 - len(fl_string)
        string = db_string + db_padding * ' ' + pl_string + pl_padding * ' ' + fl_string + fl_padding * ' '
        texts.append(string)
    buttons = []
    for j in range(len(texts)):
        buttons.append(Button(window, height=1, text=texts[j], anchor='w', font=("Courier", 14), width=60, pady=1,
                              command=lambda i=j: selectFoundWord(window_to_close, texts[i])))
    for button in buttons:
        button.pack()


def findWord():
    connection = sqlite3.connect(foreignDatabase)
    cursor = connection.cursor()
    word_category = getEnglishWordCategory()
    if word_category != 'all':
        select_query, where_query, find_query = buildQuery('find')
        # cursor.execute(select_query)
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
        for category in validWordCategoryList:
            select_query, where_query, find_query = buildQuery('find', category + 's')
            cursor.execute(find_query)
            print(find_query)
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
        found_word_window = createFoundWordsWindow()
        found_word_window.geometry('680x500')
        master.resizable(width=False, height=False)

        main_frame = Frame(found_word_window)
        main_frame.pack(fill=BOTH, expand=1)

        some_canvas = Canvas(main_frame)
        some_canvas.pack(side=LEFT, fill=BOTH, expand=1)

        scrollbar = ttk.Scrollbar(main_frame, orient=VERTICAL, command=some_canvas.yview)
        scrollbar.pack(side=RIGHT, fill=Y)

        some_canvas.configure(yscrollcommand=scrollbar.set)
        some_canvas.bind('<Configure>', lambda e: some_canvas.configure(scrollregion=some_canvas.bbox('all')))

        second_frame = Frame(some_canvas)

        some_canvas.create_window((0, 0), window=second_frame, anchor='nw')

        def on_mousewheel(event):
            try:
                if some_canvas.yview() == (0.0, 1.0):
                    return
                some_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
            except _tkinter.TclError:
                return

        some_canvas.bind_all("<MouseWheel>", on_mousewheel)

        tag_words = createTagWordsList(tagsValueList, normal_symbols)
        if strictTagsValue.get():
            for i in range(len_categories - 1, -1, -1):
                restrictWordsToStrictTags(result[i], tag_words)
                if len(result[i]) == 0:
                    del result_categories[i]
                    del result[i]
                    len_categories -= 1
        for i in range(len_categories - 1, -1, -1):
            packWordsFoundInTable(second_frame, found_word_window, result_categories[i], result[i])

        def on_closing():
            enableButtons()
            enableEntriesAndDropdown()
            found_word_window.destroy()

        found_word_window.protocol("WM_DELETE_WINDOW", on_closing)
    connection.commit()
    connection.close()


def addTagsToQuery(no_conditions, query, tag_words):
    if no_conditions > 0:
        query += ' AND '
    tag_range = '\', \''.join(tag_words)
    query += f'(tag{1} in (\'{tag_range}\')'
    for i in range(1, len(tagsValueList)):
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
    connection = sqlite3.connect(foreignDatabase)
    cursor = connection.cursor()
    cursor.execute(f'select * from {database} LIMIT 1;')
    names = [description[0] for description in cursor.description]
    connection.commit()
    connection.close()
    return names


def updateSuggestedTagsEntryLists(new_tags_list):
    for tag_entry in wordTagEntryList:
        tag_entry['completevalues'] = new_tags_list
    availableTagsList['values'] = new_tags_list


def addWord():
    global availableLabels
    word_category = getEnglishWordCategory()
    if word_category == "all":
        messagebox.showwarning("missing data", "You NEED to select one of the available WORD CATEGORY!")
        return None
    if checkIfPolishAndForeignWordsFilled():
        database = word_category + "s"
        connection = sqlite3.connect(foreignDatabase)
        cursor = connection.cursor()
        result = cursor.execute(f'select * from {database} LIMIT 1;')
        names = [description[0] for description in result.description]
        query = f"INSERT INTO {database} VALUES (:{', :'.join(names)})"
    else:
        messagebox.showwarning("missing data", f"You NEED to fill POLISH AND {taughtLanguage.upper()} WORD entries!")
        return None
    new_polish_word = getPolishWord()
    new_foreign_word = getForeignWord()
    if word_category == 'basic':
        query_dictionary = {f'polish_word': new_polish_word,
                            f'{taughtLanguage}_word': new_foreign_word}
    else:
        query_dictionary = {f'polish_{word_category}': new_polish_word,
                            f'{taughtLanguage}_{word_category}': new_foreign_word}
    if word_category == "noun":
        gender = getEnglishNounGender()
        if gender == '-':
            messagebox.showwarning("missing data", "You NEED to specify GENDER of the noun!")
            return
        query_dictionary[f'{taughtLanguage}_gender'] = gender
    elif word_category == "verb":
        for i in range(len(verbEntryList)):
            verb_value = verbEntryList[i].get().lower().strip()
            if len(verb_value) == 0:
                query_dictionary[db_verb_list[i]] = None
            else:
                query_dictionary[db_verb_list[i]] = f'{verb_value}'
    word_tags_list = []
    for i in range(len(tagsValueList)):
        tag = tagsValueList[i].get().lower().strip()
        word_tags_list.append(tag)
        if len(tag) == 0:
            query_dictionary[f'tag{i + 1}'] = None
        else:
            query_dictionary[f'tag{i + 1}'] = f'{tag}'
    query_dictionary['difficulty'] = f'{getEnglishDifficulty()}'
    try:
        cursor.execute(query, query_dictionary)
        messagebox.showinfo('Success', 'Word has been added!')
        availableLabels = addUniqueFromListToList(availableLabels, word_tags_list)
        availableLabels.sort()
        updateSuggestedTagsEntryLists(availableLabels)
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
    if checkIfPolishAndForeignWordsFilled():
        select_query_part, where_query_part, update_query_part = buildQuery('change')
    else:
        messagebox.showwarning("missing data", f"You NEED to fill POLISH AND {taughtLanguage.upper()} WORD entries!")
        return
    find_query = select_query_part + where_query_part
    connection = sqlite3.connect(foreignDatabase)
    cursor = connection.cursor()
    cursor.execute(find_query)
    if len(cursor.execute(find_query).fetchall()) == 0:
        messagebox.showwarning('No words found', 'There are no desired words in the database')
        return
    middle_parts = []
    if word_category == "noun" and taughtLanguage == 'french':
        middle_parts.append(f'{taughtLanguage}_gender = \'{getEnglishNounGender()}\'')
    elif word_category == "verb":
        for i in range(len(verbEntryList)):
            conjugated_verb = verbEntryList[i].get().lower().strip()
            if len(conjugated_verb) == 0:
                middle_parts.append(f'{db_verb_list[i]} = NULL')
            else:
                middle_parts.append(
                    f'{db_verb_list[i]} = \'{replaceSymbolsInString(conjugated_verb, normal_symbols)}\'')
    for i in range(len(tagsValueList)):
        tag = tagsValueList[i].get().lower().strip()
        if len(tag) == 0:
            middle_parts.append(f'tag{i + 1} = NULL')
        else:
            middle_parts.append(f'tag{i + 1} = \'{replaceSymbolsInString(tag, normal_symbols)}\'')
    middle_parts.append(f'difficulty = \'{getEnglishDifficulty()}\'')
    middle = ', '.join(middle_parts)
    update_query = update_query_part + middle + where_query_part
    print(update_query)
    cursor.execute(update_query)
    connection.commit()
    connection.close()
    availableTagsList.set('')
    messagebox.showinfo('Success', 'Record successfully changed')


def removeWord():
    if getEnglishWordCategory() == "all":
        messagebox.showwarning("missing data", "You NEED to select one of the available WORD CATEGORY!")
        return
    if checkIfPolishAndForeignWordsFilled():
        select_query_part, where_query_part, delete_query = buildQuery('delete')
        connection = sqlite3.connect(foreignDatabase)
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
        messagebox.showwarning("missing data", f"You NEED to fill POLISH AND {taughtLanguage.upper()} WORD entries!")
        return


def clearMainScreen(start=False):
    for tag in tagsValueList:
        tag.set('')
    polishWord.set('')
    foreignWord.set('')
    for person in personsList:
        person.set('')
    wordDifficulty.set("-")
    if start:
        if guiLanguage.get() == 'polish':
            wordCategory.set("wszystko")
        else:
            wordCategory.set("all")
    nounGender.set("-")
    availableTagsList.set('')
    polishWordEntry.focus()


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
    if guiLanguage.get() == 'english':
        labelFramePadX.set(111)
        wordCategory.set('all')
        appMainLabelText.set('Tool for words management')
        changeLanguageText.set('Change language')
        categoryLabelText.set('Word category')
        polishWordLabelText1.set('Polish word')
        wordDifficultyLabelText1.set('Word difficulty')
        tagsLabelText.set('Tags')
        strictTagsLabelText.set('Strict tags')
        foreignNounGenderLabelText.set('French noun gender')
        if taughtLanguage == 'french':
            foreignWordLabelText1.set('French word')
            firstPersonLabelText.set('1st person')
            secondPersonLabelText.set('2nd person')
            thirdPersonLabelText.set('3rd person')
        elif taughtLanguage == 'english':
            foreignWordLabelText1.set('English word')
            firstPersonLabelText.set('1st form \n(infinitive)')
            secondPersonLabelText.set('2nd form \n(past tense)')
            thirdPersonLabelText.set('3rd form \n(past participle)')
        singularLabelText.set('Singular')
        pluralLabelText.set('Plural')
        addLabelText.set('Add')
        findLabelText.set('Find')
        modifyLabelText.set('Modify')
        deleteLabelText.set('Delete')
        clearAllLabelText.set('Clear all')
        how_many_gender_button_times.set(2)
    else:
        labelFramePadX.set(22)
        how_many_gender_button_times.set(4)
        wordCategory.set('wszystko')
        categoryLabelText.set('Kategoria słowa')
        polishWordLabelText1.set('Polskie słowo')
        wordDifficultyLabelText1.set('Trudność słowa')
        tagsLabelText.set('Tagi')
        strictTagsLabelText.set('Dokładne tagi')
        foreignNounGenderLabelText.set('Płeć francuskiego rzeczownika')
        if taughtLanguage == 'french':
            foreignWordLabelText1.set('Francuskie słowo')
            firstPersonLabelText.set('1st osoba')
            secondPersonLabelText.set('2nd osoba')
            thirdPersonLabelText.set('3rd osoba')
        elif taughtLanguage == 'english':
            foreignWordLabelText1.set('Angielskie słowo')
            firstPersonLabelText.set('1 forma \n(infinitive)')
            secondPersonLabelText.set('2 forma \n(past tense)')
            thirdPersonLabelText.set('3 forma \n(past participle)')
        singularLabelText.set('L. pojedyncza')
        pluralLabelText.set('L. mnoga')
        addLabelText.set('Dodaj')
        findLabelText.set('Znajdź')
        modifyLabelText.set('Modyfikuj')
        deleteLabelText.set('Usuń')
        clearAllLabelText.set('Wyczyść')
        appMainLabelText.set('Narzędzie do zarządzania słowami')
        changeLanguageText.set('Zmień język')


def openMenu():
    master.destroy()
    os.system('python foreign_language_learning.py')


def prepareAvailableTagsList():
    tag_lists = createAvailableLabelsList(validWordCategoryList, tagsValueList, taughtLanguage)
    if None in tag_lists:
        tag_lists.remove(None)
    tag_lists.sort()
    return tag_lists


taughtLanguage = readTaughtLanguageFromFile()
projectDirectory, foreignDatabase = loadDirectories(taughtLanguage)

if not os.path.isfile(foreignDatabase):
    os.system(f'python create_{taughtLanguage}_database.py')

master = Tk()
frameAwayFromBorderY = 10
master.config(bg='#D2DEE6')
if taughtLanguage == 'french':
    image = projectDirectory / "images/french_flag_database.png"
    title = 'French words database'
elif taughtLanguage == 'english':
    image = projectDirectory / "images/english_flag_database.png"
    title = 'English words database'
master.title(title)
photo = PhotoImage(file=image)
master.iconphoto(True, photo)

how_many_gender_button_times = IntVar()
guiLanguage = StringVar()
guiLanguage.set(readLanguageFromFile())
labelFramePadX = IntVar()
# only one lang version uses that
labelFramePadX.set(22)

englishWordCategoryList, polishWordCategoryList, validWordCategoryList, englishWordDifficultyList, \
    polishWordDifficultyList, wordDifficulty, englishNounGenderList, polishNounGenderList, nounGender = generateBasics()

english_polish_dictionary, polish_english_dictionary, allList, basicList, verbList, nounList, adjectiveList = \
    generateDictionariesAndLanLists()

tag1, tag2, tag3, tag4, tag5, tag6, tagsValueList = generateTagVariables()

if taughtLanguage == 'french':
    polishWord, foreignWord, firstPerson, secondPerson, thirdPerson, \
        fourthPerson, fifthPerson, sixthPerson, personsList = generateEntryVariables(taughtLanguage)
elif taughtLanguage == 'english':
    polishWord, foreignWord, firstPerson, secondPerson, thirdPerson, personsList = generateEntryVariables(taughtLanguage)

wordDifficultyList, wordCategoryList, wordCategory = \
    generateDropDownLists(guiLanguage.get(), englishWordDifficultyList, polishWordDifficultyList,
                          englishWordCategoryList, polishWordCategoryList)

appMainLabelText, changeLanguageText, categoryLabelText, polishWordLabelText1, foreignWordLabelText1, \
    wordDifficultyLabelText1, tagsLabelText, strictTagsLabelText, foreignNounGenderLabelText, firstPersonLabelText, \
    secondPersonLabelText, thirdPersonLabelText, singularLabelText, pluralLabelText, addLabelText, findLabelText, \
    modifyLabelText, deleteLabelText, clearAllLabelText = generateLabelTexts()

labelTextsList = [categoryLabelText, polishWordLabelText1, foreignWordLabelText1, wordDifficultyLabelText1,
                  tagsLabelText,
                  strictTagsLabelText, foreignNounGenderLabelText, firstPersonLabelText, secondPersonLabelText,
                  thirdPersonLabelText, singularLabelText, pluralLabelText, addLabelText, findLabelText,
                  modifyLabelText, deleteLabelText, clearAllLabelText, appMainLabelText, changeLanguageText]

putMainLabels(master, appMainLabelText)


def DeployMainFrame():
    main_frame = LabelFrame(master, padx=30, pady=2)
    main_frame.grid(row=2, column=1, columnspan=2, ipady=5, sticky=E + W, pady=frameAwayFromBorderY)
    word_entry_width = 60
    word_entry_span = 4

    word_category_drop_list_label = Label(main_frame, textvariable=categoryLabelText, pady=8)
    word_category_drop_list_label.grid(row=0, column=0)
    word_category_drop_list = OptionMenu(main_frame, wordCategory, *wordCategoryList, command=ShowAppropriateEntries)
    word_category_drop_list.grid(row=0, column=1, ipadx=12)
    word_category_drop_list.config(width=7)

    word_difficulty_drop_list_label = Label(main_frame, textvariable=wordDifficultyLabelText1, pady=8)
    word_difficulty_drop_list_label.grid(row=0, column=3)
    word_difficulty_drop_list = OptionMenu(main_frame, wordDifficulty, *wordDifficultyList)
    word_difficulty_drop_list.grid(row=0, column=4, ipadx=12)
    word_difficulty_drop_list.config(width=7)

    polish_word_label = Label(main_frame, textvariable=polishWordLabelText1, pady=3)
    polish_word_label.grid(row=1, column=0)
    polish_word_entry = Entry(main_frame, width=word_entry_width, textvariable=polishWord)
    polish_word_entry.grid(row=1, columnspan=word_entry_span, column=1)

    foreign_word_label = Label(main_frame, textvariable=foreignWordLabelText1, pady=6)
    foreign_word_label.grid(row=2, column=0)
    foreign_word_entry = Entry(main_frame, width=word_entry_width, textvariable=foreignWord)
    foreign_word_entry.grid(row=2, columnspan=word_entry_span, column=1)

    return main_frame, word_category_drop_list_label, word_category_drop_list, word_difficulty_drop_list_label, \
        word_difficulty_drop_list, polish_word_label, polish_word_entry, foreign_word_label,\
        foreign_word_entry


mainFrame, wordCategoryDropListLabel, wordCategoryDropList, wordDifficultyDropListLabel, wordDifficultyDropList,\
        polishWordLabel, polishWordEntry, foreignWordLabel, foreignWordEntry = DeployMainFrame()
availableLabels = prepareAvailableTagsList()

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
wordTagEntryList = [wordTag1Entry, wordTag2Entry, wordTag3Entry, wordTag4Entry, wordTag5Entry, wordTag6Entry]

# tag specific checkbox
strictTagsValue = IntVar()
strictTagsCheckbox = Checkbutton(labelsFrame, textvariable=strictTagsLabelText, variable=strictTagsValue, bg='#EBEBD2')
strictTagsCheckbox.grid(row=2, column=1)


# tag combobox


def findFirstEmptyTagEntry():
    for index, tag_entry in enumerate(wordTagEntryList):
        if len(tag_entry.get()) == 0:
            return index
    return -1


def tagSelected(event):
    available_tag_entry_index = findFirstEmptyTagEntry()
    if available_tag_entry_index != -1:
        tagsValueList[available_tag_entry_index].set(newTagValue.get())


newTagValue = StringVar()
availableTagsList = ttk.Combobox(labelsFrame, textvariable=newTagValue, width=tagEntryWidth, state='readonly'
                                 , values=[''] + availableLabels)
availableTagsList.grid(row=2, column=3)
availableTagsList.bind("<<ComboboxSelected>>", tagSelected)

# Category specific frame
categorySpecificFrame = LabelFrame(master, padx=labelFramePadX.get(), pady=2, bg='#F0D3AC')

# Noun specific labels and entries
foreignGenderLabel = Label(categorySpecificFrame, textvariable=foreignNounGenderLabelText, bg='#F0D3AC')
foreignGender = OptionMenu(categorySpecificFrame, nounGender, *polishNounGenderList)
# Verb specific labels and entries
if taughtLanguage == 'french':
    db_verb_list = ['first_person', 'second_person', 'third_person',
                    'fourth_person', 'fifth_person', 'sixth_person']
elif taughtLanguage == 'english':
    db_verb_list = ['first_form', 'second_form', 'third_form']

personEntryWidth = 25

firstPersonLabel = Label(categorySpecificFrame, textvariable=firstPersonLabelText, bg='#F0D3AC')
firstPersonEntry = Entry(categorySpecificFrame, width=personEntryWidth, textvariable=firstPerson)
secondPersonLabel = Label(categorySpecificFrame, textvariable=secondPersonLabelText, bg='#F0D3AC')
secondPersonEntry = Entry(categorySpecificFrame, width=personEntryWidth, textvariable=secondPerson)
thirdPersonLabel = Label(categorySpecificFrame, textvariable=thirdPersonLabelText, bg='#F0D3AC')
thirdPersonEntry = Entry(categorySpecificFrame, width=personEntryWidth, textvariable=thirdPerson)
if taughtLanguage == 'french':
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
elif taughtLanguage == 'english':
    verbLabelsList = [firstPersonLabel, secondPersonLabel, thirdPersonLabel]
    verbEntryList = [firstPersonEntry, secondPersonEntry, thirdPersonEntry]
    verbVariableList = [firstPerson, secondPerson, thirdPerson]
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
if taughtLanguage == 'french':
    entriesList = [polishWordEntry, foreignWordEntry, firstPersonEntry, secondPersonEntry,
                   thirdPersonEntry, fourthPersonEntry, fifthPersonEntry, sixthPersonEntry,
                   wordTag1Entry, wordTag2Entry, wordTag3Entry, wordTag4Entry, wordTag5Entry, wordTag6Entry]
elif taughtLanguage == 'english':
    entriesList = [polishWordEntry, foreignWordEntry, firstPersonEntry, secondPersonEntry, thirdPersonEntry,
                   wordTag1Entry, wordTag2Entry, wordTag3Entry, wordTag4Entry, wordTag5Entry, wordTag6Entry]
dropdownsList = [wordCategoryDropList, wordDifficultyDropList, foreignGender]

# master.geometry(f"680x200")
adjustToLanguage()
clearMainScreen(True)
master.resizable(width=False, height=False)
master.mainloop()
