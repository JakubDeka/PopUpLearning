from auxiliary import *

projectDirectory, frenchDatabase = loadDirectories()
connection = sqlite3.connect(frenchDatabase)
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE basics (
    polish_word text NOT NULL,
    french_word text NOT NULL,
    difficulty text,
    tag1 text,
    tag2 text,
    tag3 text,
    tag4 text,
    tag5 text,
    tag6 text,
    PRIMARY KEY(polish_word, french_word)
    )
    """)

cursor.execute("""
    CREATE TABLE nouns (
    polish_noun text NOT NULL,
    french_noun text NOT NULL,
    french_gender text NOT NULL,
    difficulty text,
    tag1 text,
    tag2 text,
    tag3 text,
    tag4 text,
    tag5 text,
    tag6 text,
    PRIMARY KEY(polish_noun, french_noun)
    )
    """)

cursor.execute("""
    CREATE TABLE verbs (
    polish_verb text NOT NULL,
    french_verb text NOT NULL,
    first_person text,
    second_person text,
    third_person text,
    fourth_person text,
    fifth_person text,
    sixth_person text,
    difficulty text,
    tag1 text,
    tag2 text,
    tag3 text,
    tag4 text,
    tag5 text,
    tag6 text,
    PRIMARY KEY(polish_verb, french_verb)
    )
    """)

cursor.execute("""
    CREATE TABLE adjectives (
    polish_adjective text NOT NULL,
    french_adjective text NOT NULL,
    difficulty text,
    tag1 text,
    tag2 text,
    tag3 text,
    tag4 text,
    tag5 text,
    tag6 text,
    PRIMARY KEY(polish_adjective, french_adjective)
    )
    """)

connection.commit()
connection.close()
