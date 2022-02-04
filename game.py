import re
import timeit
from collections import Counter
from typing import List

from PyDictionary import PyDictionary
from textwrap import dedent
from translate import Translator
from word import Word


class Game:
    def __init__(self):
        self.bw1_word_list = []
        self.bw2_word_list = []
        self.py_dictionary = PyDictionary()
        self.translator = Translator(to_lang="vi")
        with open("dict/bw1.txt") as file1:
            for line in file1:
                self.bw1_word_list.append(Word(line.strip()))

        with open("dict/bw2.txt") as file2:
            for line in file2:
                self.bw2_word_list.append(Word(line.strip()))

    @staticmethod
    def is_word_subset_input(input_letter: List[str], word: List[str], missing_limit=0):
        # get counts of two lists
        count_input = Counter(input_letter)
        count_word = Counter(word)
        missing = 0
        for key in count_word:
            if count_word[key] > count_input[key]:
                missing += (count_word[key] - count_input[key])
        return missing <= missing_limit

    @staticmethod
    def welcome():
        print(dedent("""
            Chào mừng bạn
            Đây là phần mềm hỗ trợ chơi game Bookworm adventures (vol1, vol2)
            Để tìm từ dài nhất khi chơi adventures, bạn gõ câu lệnh sau:
            venv/bin/python3 main.py longest-word <bw1/bw2> <input>
            hoặc
            venv/bin/python3 main.py longest-word <bw1/bw2> <input> -m <missing-limit> -o <output-limit>
            Để chơi minigame word master, ta gõ như sau:
            venv/bin/python3 main.py word-master <bw1/bw2> <pattern> <available> -m <missing>
            Để chơi minigame mutant-word, ta gõ như sau:
            venv/bin/python3 main.py mutant-word <input>
            Nếu cần rút gọn prompt, gõ: PS1='command$ '
        """))

    def longest_word(self, game_mode: str, input_str: str, missing_limit: int = 0, output_limit: int = 5):
        start = timeit.default_timer()
        input_char = list(input_str)
        if game_mode == "bw1":
            word_list = self.bw1_word_list
        else:
            word_list = self.bw2_word_list
        result = []
        for word in word_list:
            word_2 = word.word.replace("qu", "q")
            word_char = list(word_2)
            if self.is_word_subset_input(input_char, word_char, missing_limit):
                result.append(word)

        result.sort(key=lambda w: w.weight, reverse=True)

        print("Danh sách các từ dài nhất")
        for i in range(output_limit):
            meaning = str(self.py_dictionary.meaning(result[i].word, disable_errors=True))
            translate = self.translator.translate(meaning)
            print(dedent(fr"""
                Word: {result[i].word}, weight: {result[i].weight},
                meaning: {translate}
            """))
        stop = timeit.default_timer()
        print('Thời gian chạy: ', stop - start)

    def word_master(self, game_mode: str,
                    pattern: str,
                    available: str,
                    missing: str = ""):
        start = timeit.default_timer()
        if game_mode == "bw1":
            word_list = self.bw1_word_list
        else:
            word_list = self.bw2_word_list
        result = []
        pattern_1_list = list(pattern)
        for index, char in enumerate(pattern_1_list):
            if char == "_":
                if available[index] != "_":
                    pattern_1_list[index] = f"[^{missing}{available[index]}]"
                else:
                    pattern_1_list[index] = f"[^{missing}]"
        pattern_1 = "".join(pattern_1_list)
        pattern_2 = f"{pattern}{available}".replace("_", "")
        for word in word_list:
            condition_1 = len(word.word) == 5
            condition_2 = re.search(pattern_1, word.word) is not None
            condition_3 = self.is_word_subset_input(list(word.word), list(pattern_2))
            if condition_1 and condition_2 and condition_3:
                result.append(word)
        print(f"Số lượng các từ thỏa mãn yêu cầu: {len(result)}")
        for word in result:
            meaning = self.py_dictionary.meaning(word.word, disable_errors=True)
            translate = self.translator.translate(meaning)
            print(dedent(fr"""
                Word: {word.word}, 
                meaning: {translate}
            """))
        stop = timeit.default_timer()
        print('Thời gian chạy: ', stop - start)

    def mutant_word(self, input_str: str):
        start = timeit.default_timer()
        result = []
        for word in self.bw2_word_list:
            condition_1 = len(word.word) == len(input_str)
            condition_2 = self.is_word_subset_input(list(input_str), list(word.word), missing_limit=0)
            if condition_1 and condition_2:
                result.append(word)
        print(f"Số lượng các từ thỏa mãn yêu cầu: {len(result)}")
        for word in result:
            meaning = self.py_dictionary.meaning(word.word, disable_errors=True)
            translate = self.translator.translate(meaning)
            print(dedent(fr"""
                Word: {word.word}, 
                meaning: {translate}
            """))
        stop = timeit.default_timer()
        print('Thời gian chạy: ', stop - start)
