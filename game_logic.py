import random, time, os


with open('russian-nouns.txt', 'r', encoding='utf-8') as file:
    words = tuple(word for word in file.read().split() if 4 < len(word) < 11)

game_states = (
    r'''
        -----|
        |    |
             |
             |
             |
             |
           ----
    ''',
    r'''
        -----|
        |    |
        O    |
             |
             |
             |
           ----
    ''',
    r'''
        -----|
        |    |
        O    |
        |    |
             |
             |
           ----
    ''',
    r'''
        -----|
        |    |
        O    |
       \|    |
             |
             |
           ----
            ''',
    r'''
        -----|
        |    |
        O    |
       \|/   |
             |
             |
           ----
    ''',
    r'''
        -----|
        |    |
        O    |
       \|/   |
        |    |
       /     |
           ----
    ''',
    r'''
        -----|
        |    |
        O    |
       \|/   |
        |    |
       / \   |
           ----
    '''
)

russian_alphabet = [chr(i) for i in range(ord('а'), ord('а') + 32)]


def get_word_state_and_letters_index(secret_word: str) -> tuple:
    letters_index = {}

    for i, letter in enumerate(secret_word):
        letters_index.setdefault(letter, []).append(i)

    word_state = ['_' for _ in range(len(secret_word))]

    return word_state, letters_index


def game_cycle() -> bool:
    used_letters = []

    attempts_counter = 0
    secret_word = random.choice(words)

    word_state, letters_index = get_word_state_and_letters_index(secret_word)

    print(f'Загаданное слово состоит из {len(secret_word)} букв.', end='\n\n')

    while attempts_counter < 6 and ''.join(word_state) != secret_word:
        letter = input('Введите букву русского алфавита: ')

        if letter in used_letters:
            print(f'Вы уже проверяли наличие буквы {letter} в слове.', end='\n\n')
            continue

        if letter not in russian_alphabet:
            print('Проверьте расскладку клавиатуры.', end='\n\n')
            continue

        used_letters.append(letter)

        if letter in secret_word:
            print(f'Да, буква "{letter}" есть в слове!')

            for i in letters_index[letter]:
                word_state[i] = letter

            print(''.join(word_state))

        else:
            print(f'К сожалению, буквы "{letter}" нет в слове.')
            attempts_counter += 1
            print(game_states[attempts_counter])

    return not attempts_counter == 6


def game():
    while True:
        if game_cycle():
            print('Поздравляю, вы отгадали слово!', end='\n\n')
        else:
            print('Вы проиграли.', end='\n\n')
        game_continue = input('Если вы хотите сыграть еще раз введите "да": ').lower()
        if game_continue == 'да':
            continue
        exit()

