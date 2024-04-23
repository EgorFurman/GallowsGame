import random
import re
from typing import Any, NoReturn
from game_messages import GallowsGameMessages as Msg
from gallows_states import gallows_states


__errors_count_default: int = 6  # максимально допустимое количество ошибок в игре.


def is_russian_symbol(symbol: Any) -> bool:
    """
    Функция для проверки принадлежности символа русскому алфавиту.

    Принимает один аргумент:
    symbol (str): Строка состоящая из одного символа.

    Возвращает логическое значение: True, если символ принадлежит русскому алфавиту, иначе False.
    """
    return isinstance(symbol, str) and re.match(r'^[а-яА-Я]$', symbol)


def get_secret_word() -> str:
    """
    Функция для подгрузки случайно выбранного слова из словаря для дальнейшего использования в игре.

    Возвращает secret_word (str): Слово(существительное) русского языка.
    """
    with open('russian-nouns.txt', 'r', encoding='utf-8') as file:
        secret_word = random.choice(file.read().split())
    return secret_word


def mask_word(secret_word: str) -> list[str]:
    """
    Функция для получения слова.

    Принимает один аргумент:
    secret_word (str): Секретное слово.

    Возвращает mask_word (list[str]): Список длинны len(secret_word), где каждой букве поставлен в соответствие символ "-".
    """
    return ['-' for _ in secret_word]


def get_letter_indices(secret_word: str) -> dict[str, list[int]]:
    """
    Функция для получения словаря letter_indices, ключами которого служат буквы слова secret_word,
    а значениями списки с индексами вхождения данной буквы в слово secret_word.

    Принимает один аргумент:
    secret_word (str): Секретное слово.

    Возвращает letter_indices (dict): Cловарь,
    в котором буквам слова, сопоставлены списки с индексами вхождения данных букв в слово.
    """
    letter_indices = {}

    for i, letter in enumerate(secret_word):
        letter_indices.setdefault(letter, []).append(i)

    return letter_indices


def print_with_double_indent(*args, **kwargs):
    """
    Функция print, но с двойным переносом строки.
    """
    print(*args, **kwargs, end='\n\n')


def is_word_guessed(masked_word: list[str], secret_word: str) -> bool:
    """
    Функция для проверки соответствия замаскированного слова секретному.

    Принимает два аргумента:
    masked_word (list), secret_word (str): Замаскированное слово, секретное слово.

    Возвращает логическое значение: True если замаскированное слово равно секретному, иначе False.
    """
    return ''.join(masked_word) == secret_word


def sub_letters_into_maskword(indices: dict[str: [int]], masked_word: list[str], letter: str) -> None:
    """
    Функция для подстановки букв в замаскированное слово.

    Принимает три аргумента:
    indices (dict), masked_word (list), letter (str): Словарь с индексами вхождения букв в слово, замаскированное слово,
    буква.

    Функция подставляет отгаданную букву (letter) в список (masked_word) по индексам соответствующим вхождению данной
    буквы в исходное слово indices[letter].
    """
    for i in indices[letter]:
        masked_word[i] = letter


def is_win(errors_count: int) -> bool:
    """
    Функция для проверки соответствия счетчика ошибок максимально допустимому количеству ошибок.

    Принимает один аргумент: errors_counter (int).

    Возвращает логическое значение: True если счетчик ошибок не равен максимально допустимому количеству ошибок,
    иначе False.
    """
    return errors_count != __errors_count_default


def play_one_game() -> None:
    """
    Функция реализует одну игровую партию.

    При вызове инициализируются переменные: secret_word - загаданное слово, masked_word - замаскированное слово,
    letter_indices - индексы вхождения букв в слово, verified_letters - проверенные пользователем буквы,
    errors_counter - счетчик ошибок.

    Далее запускается игровой цикл, который будет выполняться, пока счетчик ошибок меньше максимально допустимого числа
    ошибок.

    Во время каждой итерации, программа запрашивает пользователя букву, которая в свою очередь проверятся на
    принадлежность русскому алфавиту, а также непринадлежность проверенным ранее буквам. Если буква проходит проверки,
    то программа проверяет истинность вхождения данной буквы в слово - в случае положительного ответа, происходит
    подстановка буквы в замаскированное слово, иначе счетчик ошибок увеличивается на единицу.

    Также пользователь получает сообщения о наличие или отсутствие в слове предполагаемой буквы, текущем состояние
    виселицы(в случае ошибки), состояние замаскированного слова.

    Цикл завершается, если счетчик ошибок становится равен максимально допустимому числу ошибок или если
    замаскированное слово равняется исходному(загаданному).

    После завершения цикла функция выводит сообщение о победе или поражении, в случае если счетчик ошибок не равен
    максимальному соответственно.
    """
    secret_word = get_secret_word()

    masked_word = mask_word(secret_word)
    letter_indices = get_letter_indices(secret_word=secret_word)

    verified_letters = []
    errors_counter = 0

    print_with_double_indent(Msg.LENGTH_OF_SECRET_WORD.format(len(secret_word)))

    while errors_counter < 6:
        letter = input(Msg.INPUT_LETTER_MESSAGE)\

        if not is_russian_symbol(symbol=letter):
            print_with_double_indent(Msg.CHECK_KEYBOARD_LAYOUT)
            continue

        if letter in verified_letters:
            print_with_double_indent(Msg.VERIFIED_LETTER.format(letter))
            continue

        verified_letters.append(letter)

        if letter in secret_word:
            print(Msg.CORRECT_LETTER.format(letter))

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


def is_game_continue() -> bool:
    """
    Функция запрашивает пользователя сообщение о желании продолжить игру, если ответ положительный("да") возвращает True,
    иначе False.
    """
    return input(Msg.IS_GAME_CONTINUE).lower() == 'да'


def start_game_cycle() -> NoReturn:
    """
    Функция запускает игровой цикл(бесконечный). В каждой итерации которого, последовательно происходит вызов функция play_one_game,
    is_game_continue. В зависимости от возвращенного функцией is_game_continue значения происходит очередная итерация или
    выход из игры.
    """
    print(Msg.GREETING)

    while True:
        play_one_game()
        is_continue = is_game_continue()
        if not is_continue:
            exit()
        print(Msg.CONTINUE)
        continue


if __name__ == '__main__':
    start_game_cycle()


