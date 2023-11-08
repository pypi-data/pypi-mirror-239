import random

class SimpleWordle:
    def __init__(self, word_list, word_length=5):
        self.word_list = [word.upper() for word in word_list if len(word) == word_length]
        self.target_word = random.choice(self.word_list)
        self.word_length = word_length
        self.attempts = 0

    def guess(self, word):
        word = word.upper()
        if len(word) != self.word_length:
            return "Invalid word length."
        self.attempts += 1
        feedback = []
        for i, char in enumerate(word):
            if char == self.target_word[i]:
                feedback.append('🟩')
            elif char in self.target_word:
                feedback.append('🟨')
            else:
                feedback.append('⬛')
        return ''.join(feedback)

    def play(self):
        while self.attempts < 6:
            user_guess = input(f"Attempt {self.attempts + 1}/6: Enter your guess: ").upper()
            feedback = self.guess(user_guess)
            print(feedback)
            if user_guess == self.target_word:  # This comparison is now case-insensitive
                print(f"Congratulations! You've guessed the word in {self.attempts} attempts.")
                return 1
        print(f"Sorry, you didn't guess the word. The correct word was {self.target_word}.")
        return 0

# A function to create and start the game
def start_game(word_list_path='word_list.txt'):
    with open(word_list_path, 'r') as file:
        word_list = file.read().splitlines()
    game = SimpleWordle(word_list)
    game.play()
    return 0

# A function to add a word to the word list
def add_word(word, word_list_path):
    with open(word_list_path, 'a') as file:
        file.write(f"{word.upper()}\n")
    print(f"Added {word.upper()} to the word list.")

# A function to remove a word from the word list
def remove_word(word, word_list_path):
    with open(word_list_path, 'r') as file:
        words = file.read().splitlines()
    if word.upper() in words:
        words.remove(word.upper())
        with open(word_list_path, 'w') as file:
            file.writelines("\n".join(words))
        print(f"Removed {word.upper()} from the word list.")
    else:
        print(f"{word.upper()} was not found in the word list.")

# A function to show the word list
def show_word_list(word_list_path):
    with open(word_list_path, 'r') as file:
        words = file.read().splitlines()
    for word in words:
        print(word)
