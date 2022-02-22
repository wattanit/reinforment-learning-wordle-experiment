from Dictionary import *
import random

class Wordle:
    def __init__(self, dict="extended"):
        self.dict = Dictionary(dict)
        self.answer = self.dict.get_random_words()
        self.attempt = 0
        self.stage = "_____"
        self.used_characters = set()
        self.found_characters = set()

    def play_word(self, word):
        if len(word) != 5:
            print("Invalid word: must be 5 characters")
            return
        if not self.dict.has_word(word):
            print("Invalid word: not in dictionary")
            return

        self.attempt += 1

        if self.answer == word:
            self.stage = word
            return True, "Win"
        else:
            stage = ""
            for i in range(0, len(word)):
                if word[i] == self.answer[i]:
                    stage += self.answer[i]
                else:
                    stage += "_"

                    if self.answer.__contains__(word[i]):
                        self.found_characters.add(word[i])
                    else:
                        self.used_characters.add(word[i])

            self.stage = stage

            if self.attempt == 6:
                return True, "Lose"
            else:
                return False, None

    def self_play(self):
        is_over = False
        while not is_over:
            available_words = self.dict.get_words(
                letters="".join(self.found_characters),
                ban_letters="".join(self.used_characters),
                template=self.stage
            )
            guess = random.choice(available_words)

            is_over, result = self.play_word(guess)
            print("{}: {} : guessed {}".format(self.attempt-1, self.stage, guess))
            print("Found letters: {}".format(self.found_characters))
            print("Used letters: {}".format(self.used_characters))

            if is_over:
                print()
                print("Done. You {}. {}/6".format(result, self.attempt))
                if result == "Win":
                    return True
                else:
                    return False
