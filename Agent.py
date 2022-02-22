from __future__ import annotations
import pandas as pd
import random
from Wordle import *

learning_rate = 0.8
discount_rate = 0.2
reward_table = {
    'win': 100.0,
    'green' : 20.0,
    'yellow' : 1.0,
    'grey': -10.0,
}

class Agent:
    def __init__(self):
        self.q_table = pd.DataFrame(columns=['state','word','value'])
        self.dictionary = Dictionary(dict='common')
        self.game_count = 0
        self.game_win = 0
        self.step_total = 0
        self.win_stats = []
        self.new_game()


    def new_game(self):
        self.game = Wordle(dict='common')
        self.state = self.game.stage
        self.step_count = 0
        self.found_letters = set()
        self.used_letters = set()

    def map_index_to_char(self, index: int)-> str:
        mapper = {
            0: 'a',
            1: 'b',
            2: 'c',
            3: 'd',
            4: 'e',
            5: 'f',
            6: 'g',
            7: 'h',
            8: 'i',
            9: 'j',
            10: 'k',
            11: 'l',
            12: 'm',
            13: 'n',
            14: 'o',
            15: 'p',
            16: 'q',
            17: 'r',
            18: 's',
            19: 't',
            20: 'u',
            21: 'v',
            22: 'w',
            23: 'x',
            24: 'y',
            25: 'z'
        }
        return mapper.get(index, '')

    def map_char_to_index(self, char: str)-> int:
        mapper = {
            'a': 0,
            'b': 1,
            'c': 2,
            'd': 3,
            'e': 4,
            'f': 5,
            'g': 6,
            'h': 7,
            'i': 8,
            'j': 9,
            'k': 10,
            'l': 11,
            'm': 12,
            'n': 13,
            'o': 14,
            'p': 15,
            'q': 16,
            'r': 17,
            's': 18,
            't': 19,
            'u': 20,
            'v': 21,
            'w': 22,
            'x': 23,
            'y': 24,
            'z': 25
        }
        return mapper.get(char, '')

    def guess_word_on_policy(self)-> str|None:
        # get possible words list
        guess_words = self.dictionary.get_words(template=self.state, letters=self.found_letters, ban_letters=self.used_letters)
        if len(guess_words) == 0:
            return None

        if not self.state in self.q_table['state'].values:
            # constructing Q values for this state
            new_entries = []
            for word in self.dictionary.get_words(template=self.state):
                new_entries.append((self.state, word, 0.0))
            self.q_table = pd.concat([self.q_table, pd.DataFrame(new_entries, columns=['state','word','value'])]).reset_index(drop=True)

        # find best guess
        if random.random() <= 0.6:
            best_value = self.q_table[self.q_table['state']==self.state]['value'].max()
            best_guess_words_df = self.q_table[(self.q_table['state']==self.state) & (self.q_table['value']==best_value)]
            best_guess_words = best_guess_words_df['word'].values

            guess_word = random.choice(best_guess_words)
        else:
            guess_word = random.choice(guess_words)

        return guess_word

    def step(self):
        self.step_count += 1
        self.step_total += 1

        guess_word = self.guess_word_on_policy()
        if not guess_word:
            return True, "Lose"

        # play a wordle turn
        is_over, result = self.game.play_word(guess_word)
        next_state = self.game.stage

        if is_over:
            if result == "Win":
                self.game_win += 1
                target_update = (self.q_table['state'] == self.state) & (self.q_table['word'] == guess_word)
                old_q = self.q_table[target_update]['value']
                self.q_table.loc[target_update, 'value'] = old_q + learning_rate * (reward_table['win'])

            self.state = next_state
            self.game_count += 1
            return True, result

        # update Q Table : look ahead reward
        if next_state in self.q_table['state'].values:
            look_ahead_reward = self.q_table[self.q_table['state']==next_state]['value'].max()
        else:
            look_ahead_reward = 0.0

        # update Q Table : compute reward

        correct_letters = [c for c in self.game.stage if c != "_" ]
        found_letters = self.game.found_characters
        used_letters = self.game.used_characters

        reward = reward_table['green']*len(correct_letters) + \
                 reward_table['yellow']*len(found_letters) + \
                 reward_table['grey']*len(used_letters)

        target_update = (self.q_table['state']==self.state) & (self.q_table['word']==guess_word)
        old_q = self.q_table[target_update]['value'].iloc[0]

        # update Q Table : update Q value
        self.q_table.loc[target_update,'value'] = old_q + learning_rate*(reward + discount_rate*look_ahead_reward)

        # update state
        self.state = next_state
        self.found_letters = found_letters
        self.used_letters = used_letters

        return False, None

    def train(self, n=500, print_freq=1):
        for i in range(0, n):
            if (self.game_count % print_freq)==0:
                print("Game {}".format(self.game_count+1))

            self.new_game()
            is_over = False
            result = None
            while not is_over:
                is_over, result = self.step()

            self.win_stats.append(self.game_win/self.game_count)

            if (self.game_count % print_freq) == 0:
                print("Game over: {} | total attempts: {}, total guess {}".format(result, self.game.attempt, self.step_count))
                print("Total game: {} | Total win: {} ({}%)".format(self.game_count, self.game_win, 100*self.game_win/self.game_count))
                print("-------------------------------------------------------------")
