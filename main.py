import random
from game_messages import GallowsGameMessages as Msg
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
    return input(Msg.IS_GAME_CONTINUE).lower() == 'да'


def is_win(errors_count: int) -> bool:
    return errors_count != errors_count_default


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
        letter = input(Msg.INPUT_LETTER_MESSAGES)

        if letter not in russian_alphabet:
            print_with_double_indent(Msg.CHECK_KEYBOARD_LAYOUT)
            continue

        if letter in used_letters:
            print_with_double_indent(Msg.REPEATING_LETTER.format(letter))
            continue

        used_letters.append(letter)

        if letter in secret_word:
            print(Msg.CORRECT_LETTER.format(letter))

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


def game_cycle():
    while True:
        secret_word = get_secret_word()
        errors_count = get_errors_count(secret_word)
        if is_win(errors_count):
            print_with_double_indent(Msg.IS_WIN)
        else:
            print_with_double_indent(Msg.IS_FAIL, Msg.ANSWER.format(secret_word))
        if game_continue():
            continue
        exit()


if __name__ == '__main__':
    print(Msg.START_GAME)
    game_cycle()


