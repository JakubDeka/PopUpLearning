import sqlite3
from pathlib import Path
import os


projectDirectory = Path(os.getcwd()[:-5])
# foreignDatabase = projectDirectory / "french_words.db"
appSettings = projectDirectory / "settings.txt"
tagLength = 6


def loadDirectories(taught_language):
    return projectDirectory, projectDirectory / f"{taught_language}_words.db"


def generateNormalAndStrangeSymbolDicts():
    normal_symbols = {'\'': 'ƥ', '\"': 'ƣ'}
    strange_symbols = {}
    for key, value in normal_symbols.items():
        strange_symbols[value] = key
    return normal_symbols, strange_symbols


def replaceSymbolsInString(string, symbols_dictionary):
    for symbol in symbols_dictionary:
        string = string.replace(symbol, symbols_dictionary[symbol])
    return string


def intersection(list_1, list_2):
    temp = set(list_2)
    list_3 = [value for value in list_1 if value in temp]
    return list_3


def restrictWordsToStrictTags(word_list, tag_words):
    for i, e in reversed(list(enumerate(word_list))):
        word_tags = e[-tagLength:]
        common_tags = intersection(word_tags, tag_words)
        if len(common_tags) != len(tag_words):
            del word_list[i]


def createTagWordsList(tag_list, symbols_dictionary):
    tag_words_list = [replaceSymbolsInString(tag.get().lower(), symbols_dictionary) for tag in tag_list
                      if (len(tag.get()) > 0)]
    return tag_words_list


def addUniqueFromListToList(old_list, new_list):
    for element in new_list:
        if element not in old_list:
            old_list.append(element)
    return old_list


def uniqueValuesInListLike(list_like):
    list_set = set(list_like)
    return list(list_set)


def createAvailableLabelsList(valid_word_category_list, tags_list, taught_language):
    project_directory, foreign_database = loadDirectories(taught_language)
    connection = sqlite3.connect(foreign_database)
    cursor = connection.cursor()
    labels_list = []
    for word_category in valid_word_category_list:
        database = word_category + 's'
        query = 'SELECT '
        for i in range(len(tags_list)):
            query += f'tag{i + 1}'
            if i < len(tags_list) - 1:
                query += ', '
        query += f' FROM {database}'
        cursor.execute(query)
        for row in cursor.fetchall():
            labels_list += uniqueValuesInListLike(row)
        labels_list = uniqueValuesInListLike(labels_list)
    connection.commit()
    connection.close()
    return labels_list


def generateDictionariesAndLanLists():
    english_polish_dictionary = {'all': 'wszystko', 'basic': 'podstawowe', 'noun': 'rzeczownik', 'verb': 'czasownik',
                                 'adjective': 'przymiotnik', 'easy': 'łatwe', 'medium': 'średnie', 'hard': 'trudne',
                                 'masculine': 'męska', 'feminine': 'żeńska', 'Add': 'Dodaj', 'Find': 'Znajdź',
                                 'Modify': 'Modyfikuj', 'Delete': 'Usuń', 'Clear all': 'Wyczyść',
                                 'Word category': 'Kategoria słowa', 'Polish word': 'Polskie słowo',
                                 'French word': 'Francuskie słowo', 'Word difficulty': 'Trudność słowa', 'Tags': 'Tagi',
                                 'Strict tags': 'Dokładne tagi', 'French noun gender': 'Płeć francuskiego rzeczownika',
                                 '1st person': '1st osoba', '2nd person': '2nd osoba', '3rd person': '3rd osoba',
                                 'Singular': 'L. pojedyncza', 'Plural': 'L. mnoga',
                                 'Words database actions': 'Akcje bazy danych',
                                 'Tool for words management': 'Narzędzie do zarządzania słowami',
                                 'Change language': 'Zmień język', '-': '-', 'Time settings': 'Ustawienia czasu',
                                 'Word settings': 'Ustawienia słów', 'hours': 'godzin', 'minutes': 'minuty',
                                 'seconds': 'sekundy', 'Word details': 'Szczegóły słowa',
                                 'Verb conjugation': 'Odmiana czasownika', 'Reset settings': 'Resetuj ustawienia',
                                 'Save new settings': 'Zapisz ustawienia',
                                 'Set available word constraints': 'Ustaw ograniczenia dostępności słów',
                                 'Time between quizzes': 'Czas pomiędzy quizami', 'Save new time': 'Zapisz czas',
                                 'Word quiz': 'Słowny quiz', 'Time until quiz': 'Czas do quizu',
                                 'Continue game': 'Kontynuuj grę', 'Stop game': 'Przestań grać',
                                 'Word \ndetails': 'Szczegóły \nsłowa', 'Word gender': 'Płeć słowa'}
    polish_english_dictionary = {}
    all_list = ['all', english_polish_dictionary['all']]
    basic_list = ['basic', english_polish_dictionary['basic']]
    verb_list = ['verb', english_polish_dictionary['verb']]
    noun_list = ['noun', english_polish_dictionary['noun']]
    adjective_list = ['adjective', english_polish_dictionary['adjective']]
    for key, value in english_polish_dictionary.items():
        polish_english_dictionary[value] = key
    return english_polish_dictionary, polish_english_dictionary, all_list, basic_list, verb_list, noun_list, \
        adjective_list


def readLanguageFromFile():
    file = open(appSettings, "r")
    line = file.readline()
    return line.split(' ')[-1].split('\n')[0]


def readTaughtLanguageFromFile():
    file = open(appSettings, "r")
    line = file.readline()
    line = file.readline()
    return line.split(' ')[-1].split('\n')[0]


def saveLanguageToFile(language):
    with open(appSettings, "r") as file:
        data = file.readlines()
    data[0] = f'language = {language}\n'
    with open(appSettings, 'w') as file:
        file.writelines(data)
