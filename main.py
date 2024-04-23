import random
import keyboard
import re
import time
import sys
from typing import Any, NoReturn
from game_messages import GallowsGameMessages as Msg
from gallows_states import gallows_states


__errors_count_default = 6


def is_russian_symbol(symbol: Any) -> bool:
    return isinstance(symbol, str) and re.match(r'^[а-яА-Я]$', symbol)


def get_secret_word() -> str:
    with open('russian-nouns.txt', 'r', encoding='utf-8') as file:
        secret_word = random.choice(file.read().split())
    return secret_word


def mask_word(secret_word: str) -> list[str]:
    return ['-' for _ in secret_word]


def get_letter_indices(secret_word: str) -> dict[str, list[int]]:
    letter_indices = {}

    for i, letter in enumerate(secret_word):
        letter_indices.setdefault(letter, []).append(i)

    return letter_indices


def print_with_double_indent(*args, **kwargs):
    print(*args, **kwargs, end='\n\n')


def is_word_guessed(masked_word: list, secret_word: str) -> bool:
    return ''.join(masked_word) == secret_word


def sub_letters_into_maskword(indices: dict[str: [int]], masked_word: list[str], letter: str) -> None:
    for i in indices[letter]:
        masked_word[i] = letter


def is_win(errors_count: int) -> bool:
    return errors_count != __errors_count_default


def some_func(char):
    return True if char == '\n' else False


def play_one_game() -> None:
    secret_word = get_secret_word()

    masked_word = mask_word(secret_word)
    letter_indices = get_letter_indices(secret_word=secret_word)

    used_letters = []
    errors_counter = 0

    print_with_double_indent(Msg.LENGTH_OF_SECRET_WORD.format(len(secret_word)))

    while errors_counter < 6:
        letter = input(Msg.INPUT_LETTER_MESSAGE)\

        if not is_russian_symbol(symbol=letter):
            print_with_double_indent(Msg.CHECK_KEYBOARD_LAYOUT)
            continue

        if letter in used_letters:
            print_with_double_indent(Msg.REPEATING_LETTER.format(letter))
            continue

        used_letters.append(letter)

        if letter in secret_word:
            print(Msg.GUESSED_LETTER.format(letter))

            sub_letters_into_maskword(indices=letter_indices, masked_word=masked_word, letter=letter)

            print_with_double_indent(''.join(masked_word))

            if is_word_guessed(masked_word=masked_word, secret_word=secret_word):
                break

        else:
            errors_counter += 1
            print(Msg.WRONG_LETTER.format(letter))
            print(''.join(masked_word))
            print(gallows_states[errors_counter])

    if is_win(errors_count=errors_counter):
        print_with_double_indent(Msg.IS_WIN)
    else:
        print_with_double_indent(Msg.IS_FAIL, Msg.ANSWER.format(secret_word))


#def get_user_continue_choice() -> bool:
#    print_with_double_indent(Msg.PRESS_THE_KEY_MESSAGE)
#
#    while True:
#        escape = keyboard.is_pressed('esc')
#        enter = keyboard.is_pressed('enter')
#        if escape:
#            return False
#        if enter:
#            return True


def get_user_continue_choice() -> bool:
    print_with_double_indent(Msg.PRESS_THE_KEY_MESSAGE)

    while True:
        event = keyboard.read_event()

        if event.event_type == keyboard.KEY_DOWN and event.name == 'esc':
            return False

        if event.event_type == keyboard.KEY_DOWN and event.name == 'enter':
            return True


def start_game_cycle() -> NoReturn:
    print(Msg.GREETING)

    while True:
        play_one_game()
        is_continue = get_user_continue_choice()
        keyboard.unhook_all()
        if not is_continue:
            exit()
        print(Msg.CONTINUE)
        continue


if __name__ == '__main__':
    start_game_cycle()


