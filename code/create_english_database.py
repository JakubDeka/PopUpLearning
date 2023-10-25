from auxiliary import *

projectDirectory, englishDatabase = loadDirectories('english')

connection = sqlite3.connect(englishDatabase)
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE basics (
    polish_word text NOT NULL,
    english_word text NOT NULL,
    difficulty text,
    tag1 text,
    tag2 text,
    tag3 text,
    tag4 text,
    tag5 text,
    tag6 text,
    PRIMARY KEY(polish_word, english_word)
    )
    """)

cursor.execute("""
    CREATE TABLE nouns (
    polish_noun text NOT NULL,
    english_noun text NOT NULL,
    difficulty text,
    tag1 text,
    tag2 text,
    tag3 text,
    tag4 text,
    tag5 text,
    tag6 text,
    PRIMARY KEY(polish_noun, english_noun)
    )
    """)

cursor.execute("""
    CREATE TABLE verbs (
    polish_verb text NOT NULL,
    english_verb text NOT NULL,
    first_form text,
    second_form text,
    third_form text,
    difficulty text,
    tag1 text,
    tag2 text,
    tag3 text,
    tag4 text,
    tag5 text,
    tag6 text,
    PRIMARY KEY(polish_verb, english_verb)
    )
    """)

cursor.execute("""
    CREATE TABLE adjectives (
    polish_adjective text NOT NULL,
    english_adjective text NOT NULL,
    difficulty text,
    tag1 text,
    tag2 text,
    tag3 text,
    tag4 text,
    tag5 text,
    tag6 text,
    PRIMARY KEY(polish_adjective, english_adjective)
    )
    """)

connection.commit()
connection.close()
