from tkinter import *
from tkinter import messagebox, ttk


def generateBasics():
    english_word_category_list = ['all', 'basic', 'noun', 'verb', 'adjective']
    polish_word_category_list = ['wszystko', 'podstawowe', 'rzeczownik', 'czasownik', 'przymiotnik']
    valid_word_category_list = english_word_category_list[1:]
    english_word_difficulty_list = ['-', 'easy', 'medium', 'hard']
    polish_word_difficulty_list = ['-', 'łatwe', 'średnie', 'trudne']
    word_difficulty = StringVar()
    english_noun_gender_list = ['-', 'masculine', 'feminine']
    polish_noun_gender_list = ['-', 'męska', 'żeńska']
    noun_gender = StringVar()
    return english_word_category_list, polish_word_category_list, valid_word_category_list, \
        english_word_difficulty_list, polish_word_difficulty_list, word_difficulty, english_noun_gender_list, \
        polish_noun_gender_list, noun_gender


def generateTagVariables():
    tag_1 = StringVar()
    tag_2 = StringVar()
    tag_3 = StringVar()
    tag_4 = StringVar()
    tag_5 = StringVar()
    tag_6 = StringVar()
    return tag_1, tag_2, tag_3, tag_4, tag_5, tag_6, [tag_1, tag_2, tag_3, tag_4, tag_5, tag_6]


def generateEntryVariables(taught_language):
    polish_word = StringVar()
    french_word = StringVar()
    first_person = StringVar()
    second_person = StringVar()
    third_person = StringVar()
    persons_list = [first_person, second_person, third_person]
    if taught_language == "french":
        fourth_person = StringVar()
        fifth_person = StringVar()
        sixth_person = StringVar()
        persons_list = persons_list + [fourth_person, fifth_person, sixth_person]
        return polish_word, french_word, \
            first_person, second_person, third_person, fourth_person, fifth_person, sixth_person, persons_list
    return polish_word, french_word, first_person, second_person, third_person, persons_list


def generateDropDownLists(gui_language, english_diff_list, polish_diff_list, english_cat_list, polish_cat_list):
    if gui_language == 'english':
        word_difficulty_list = english_diff_list
        word_category_list = english_cat_list
    elif gui_language == 'polish':
        word_difficulty_list = polish_diff_list
        word_category_list = polish_cat_list
    else:
        return
    word_category = StringVar()
    word_category.set(word_category_list[0])
    return word_difficulty_list, word_category_list, word_category


def generateLabelTexts():
    app_main_label_text = StringVar()
    change_language_text = StringVar()
    category_label_text = StringVar()
    polish_word_label_text1 = StringVar()
    french_word_label_text1 = StringVar()
    word_difficulty_label_text1 = StringVar()
    tags_label_text = StringVar()
    strict_tags_label_text = StringVar()
    french_noun_gender_label_text = StringVar()
    first_person_label_text = StringVar()
    second_person_label_text = StringVar()
    third_person_label_text = StringVar()
    singular_label_text = StringVar()
    plural_label_text = StringVar()
    add_label_text = StringVar()
    find_label_text = StringVar()
    modify_label_text = StringVar()
    delete_label_text = StringVar()
    clear_all_label_text = StringVar()
    return app_main_label_text, change_language_text, category_label_text, polish_word_label_text1, \
        french_word_label_text1, word_difficulty_label_text1, tags_label_text, strict_tags_label_text, \
        french_noun_gender_label_text, first_person_label_text, second_person_label_text, third_person_label_text, \
        singular_label_text, plural_label_text, add_label_text, find_label_text, modify_label_text, delete_label_text, \
        clear_all_label_text


def putMainLabels(window, main_text_variable):
    Label(window, textvariable=main_text_variable, font=("Arial", 20), bg='#D2DEE6').grid(row=0, column=1, ipadx=10,
                                                                                          ipady=5)
    Label(window, text='', font=("Arial", 20), bg='#D2DEE6').grid(row=0, column=0, ipadx=10, ipady=5)
    Label(window, text='', font=("Arial", 20), bg='#D2DEE6').grid(row=0, column=3, ipadx=10, ipady=5)


