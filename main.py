import random
import keyboard
import re
from typing import Any
from game_messages import GallowsGameMessages as Msg
from gallows_states import gallows_states


errors_count_default = 6


def is_russian_symbol(symbol: Any) -> bool:
    return isinstance(symbol, str) and re.match(r'^[а-яА-Я]$', symbol)


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


def print_with_double_indent(*args, **kwargs):
    print(*args, **kwargs, end='\n\n')


def is_word_guessed(masked_word: list, secret_word: str) -> bool:
    return ''.join(masked_word) == secret_word


def get_errors_count(secret_word: str) -> int:
    masked_word = mask_word(secret_word)
    letters_index = get_letters_index(secret_word)

    used_letters = []
    errors_counter = 0

    print_with_double_indent(Msg.LENGTH_OF_SECRET_WORD.format(len(secret_word)))

    while errors_counter < 6:
        letter = input(Msg.INPUT_LETTER_MESSAGE)

        if not is_russian_symbol(symbol=letter):
            print_with_double_indent(Msg.CHECK_KEYBOARD_LAYOUT)
            continue

        if letter in used_letters:
            print_with_double_indent(Msg.REPEATING_LETTER.format(letter))
            continue

        used_letters.append(letter)

        if letter in secret_word:
            print(Msg.GUESSED_LETTER.format(letter))

            for i in letters_index[letter]:
                masked_word[i] = letter

            print_with_double_indent(''.join(masked_word))

            if is_word_guessed(masked_word=masked_word, secret_word=secret_word):
                break

        else:
            print(Msg.WRONG_LETTER.format(letter))
            print(''.join(masked_word))
            errors_counter += 1
            print(gallows_states[errors_counter])

    return errors_counter


def is_win(errors_count: int) -> bool:
    return errors_count != errors_count_default


def get_user_continue_choice() -> bool:
    while True:
        escape = keyboard.is_pressed('esc')
        enter = keyboard.is_pressed('enter')

        if escape:
            return False
        if enter:
            return True


def start_game_cycle():
    print(Msg.GREETING)

    while True:
        secret_word = get_secret_word()
        errors_count = get_errors_count(secret_word)
        if is_win(errors_count):
            print_with_double_indent(Msg.IS_WIN)
        else:
            print_with_double_indent(Msg.IS_FAIL, Msg.ANSWER.format(secret_word))
        print_with_double_indent(Msg.PRESS_THE_KEY_MESSAGE)
        is_continue = get_user_continue_choice()
        keyboard.unhook_all()
        print(Msg.REPLAY)
        if not is_continue:
            exit()
        continue


if __name__ == '__main__':
    start_game_cycle()


