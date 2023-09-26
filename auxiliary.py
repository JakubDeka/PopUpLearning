tagLength = 6


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


def createTagWordsList(tag_list):
    return [tag.get().lower() for tag in tag_list if len(tag.get()) > 0]
