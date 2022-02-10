import re
import random

class Dictionary:
    def __init__(self, dict="common"):
        self.words = []
        if dict == "extended":
            with open("data/dict_extended.txt") as dict_file:
                for line in dict_file:
                    self.words.append(line.strip())
        else:
            with open("data/dict_common.txt") as dict_file:
                for line in dict_file:
                    self.words.append(line.strip())

    def count_words(self):
        return len(self.words)

    def has_word(self, word):
        return (word in self.words)

    def get_words(self, letters=None, template=None, ban_letters=None)-> list[str]:
        word_lists = self.words

        if template:
            word_lists = match_template(word_lists, template)

        if ban_letters:
            word_lists = contains_no_letters(word_lists, ban_letters)

        if letters:
            word_lists = contains_letters(word_lists, letters)

        return word_lists

    def get_random_words(self):
        return random.choice(self.words)


def match_template(word_list, template):
    if template:
        regex: str = template.replace("_", ".")
    else:
        regex = "....."

    return list(filter(lambda s: re.match(regex, s), word_list))


def contains_letters(word_list, letters):
    matched_words = set(word_list)

    for c in letters:
        matched_words =  matched_words.intersection(set(filter(lambda s: s.__contains__(c), word_list)))

    return list(matched_words)


def contains_no_letters(word_list, letters):
    matched_words = set(word_list)

    for c in letters:
        matched_words = matched_words.difference(set(filter(lambda s: s.__contains__(c), word_list)))

    return list(matched_words)