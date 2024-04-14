import random
import gallows_game_messages as msg
from gallows_states import gallows_states


russian_alphabet = ([chr(i) for i in range(ord('а'), ord('а') + 32)] +
                    [chr(i).upper() for i in range(ord('а'), ord('а') + 32)])

errors_count_default = 6


def get_secret_word() -> str:
    with open('russian-nouns.txt', 'r', encoding='utf-8') as file:
        secret_word = random.choice(file.read().split())
    return secret_word


def mask_word(secret_word: str) -> list[str]:
    return ['-' for _ in secret_word]


def get_letters_index(secret_word: str) -> dict[str, list[int]]:
    letters_index = {}

    for i, letter in enumerate(secret_word):
        letters_index.setdefault(letter, []).append(i)

    return letters_index


def game_continue() -> bool:
    return input(msg.IS_GAME_CONTINUE).lower() == 'да'


def is_win(errors_count: int) -> bool:
    return errors_count != errors_count_default


def get_errors_count(secret_word: str) -> int:
    masked_word = mask_word(secret_word)
    letters_index = get_letters_index(secret_word)

    used_letters = []
    errors_counter = 0

    print(msg.LENGTH_OF_SECRET_WORD.format(len(secret_word)), end='\n\n')

    while errors_counter < 6 and ''.join(masked_word) != secret_word:
        letter = input(msg.INPUT_LETTER_MESSAGES)

        if letter not in russian_alphabet:
            print(msg.CHECK_KEYBOARD_LAYOUT, end='\n\n')
            continue

        if letter in used_letters:
            print(msg.REPEATING_LETTER.format(letter), end='\n\n')
            continue

        used_letters.append(letter)

        if letter in secret_word:
            print(msg.CORRECT_LETTER.format(letter))

            for i in letters_index[letter]:
                masked_word[i] = letter

            print(''.join(masked_word), end='\n\n')

        else:
            print(msg.WRONG_LETTER.format(letter))
            print(''.join(masked_word))
            errors_counter += 1
            print(gallows_states[errors_counter])

    return errors_counter


def game_cycle():
    while True:
        secret_word = get_secret_word()
        errors_count = get_errors_count(secret_word)
        if is_win(errors_count):
            print(msg.IS_WIN, end='\n\n')
        else:
            print(msg.IS_FAIL, msg.ANSWER.format(secret_word), end='\n\n')
        if game_continue():
            continue
        exit()


if __name__ == '__main__':
    print('''Добро пожаловать в игру "Виселица"! 
Сейчас программа загадает слово, существительное русского языка. 
Ваша задача отгадать его прежде, чем нарисованный человек окажется на виселице. 
Вы можете играть неограниченное количество раз. Удачи!
''')
    game_cycle()


