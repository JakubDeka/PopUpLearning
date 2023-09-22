import sqlite3


connection = sqlite3.connect("french_words.db")
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE basics (
    polish_word text NOT NULL,
    french_word text NOT NULL,
    tag1 text,
    tag2 text,
    tag3 text,
    difficulty text,
    PRIMARY KEY(polish_word, french_word)
    )
    """)
cursor.execute("""
    CREATE TABLE nouns (
    polish_noun text NOT NULL,
    french_noun text NOT NULL,
    french_gender text NOT NULL,
    tag1 text,
    tag2 text,
    tag3 text,
    difficulty text,
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
    tag1 text,
    tag2 text,
    tag3 text,
    difficulty text,
    PRIMARY KEY(polish_verb, french_verb)
    )
    """)
cursor.execute("""
    CREATE TABLE adjectives (
    polish_adjective text NOT NULL,
    french_adjective text NOT NULL,
    tag1 text,
    tag2 text,
    tag3 text,
    difficulty text,
    PRIMARY KEY(polish_adjective, french_adjective)
    )
    """)
cursor.execute("""
    CREATE INDEX word_id
    on basics (polish_word, french_word);
    """)
cursor.execute("""
    CREATE INDEX id
    on nouns (polish_noun, french_noun);
    """)
# cursor.execute("""
#     CREATE INDEX id
#     on verbs (polish_verb, french_verb);
#     """)
# cursor.execute("""
#     CREATE INDEX id
#     on adjectives (polish_adjective, french_adjective);
#     """)
connection.commit()
connection.close()
