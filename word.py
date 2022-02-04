class Word:
    def __init__(self, word):
        self.word: str = word
        self.weight: float = self.calculate_word_weight(word)

    @staticmethod
    def letter_weight(letter: str) -> float:
        value = 1
        if letter in ['b', 'c', 'f', 'h', 'm', 'p']:
            value = 1.25
        elif letter in ['v', 'w', 'y']:
            value = 1.5
        elif letter in ['j', 'k', 'q']:
            value = 1.75
        elif letter in ['x', 'z']:
            value = 2
        return value

    @staticmethod
    def calculate_word_weight(word: str):
        word_list = list(word)
        weight = 0
        for letter in word_list:
            weight += Word.letter_weight(letter)
        return weight
