import random
import gallows_states

gallows_states = gallows_states.gallows_states
russian_alphabet = ([chr(i) for i in range(ord('а'), ord('а') + 32)] +
                    [chr(i).upper() for i in range(ord('а'), ord('а') + 32)])


def mask_word(secret_word: str) -> list[str]:
    return ['-' for _ in secret_word]


def get_letters_index(secret_word: str) -> dict[str, list[int]]:
    letters_index = {}

    for i, letter in enumerate(secret_word):
        letters_index.setdefault(letter, []).append(i)

    return letters_index


def get_game_result() -> bool:
    with open('russian-nouns.txt', 'r', encoding='utf-8') as file:
        secret_word = random.choice(tuple(word for word in file.read().split()))

    used_letters = []
    attempts_counter = 0

    masked_word = mask_word(secret_word)
    letters_index = get_letters_index(secret_word)

    print(f'Загаданное слово состоит из {len(secret_word)} букв.', end='\n\n')

    while attempts_counter < 6 and ''.join(masked_word) != secret_word:
        letter = input('Введите букву русского алфавита: ')

        if letter not in russian_alphabet:
            print('Проверьте раскладку клавиатуры.', end='\n\n')
            continue

        if letter in used_letters:
            print(f'Вы уже проверяли наличие буквы {letter} в слове.', end='\n\n')
            continue

        used_letters.append(letter)

        if letter in secret_word:
            print(f'Да, буква "{letter}" есть в слове!')

            for i in letters_index[letter]:
                masked_word[i] = letter

            print(''.join(masked_word), end='\n\n')

        else:
            print(f'К сожалению, буквы "{letter}" нет в слове.')
            attempts_counter += 1
            print(gallows_states[attempts_counter])
            print(''.join(masked_word))
    return attempts_counter != 6


def game():
    while True:
        if get_game_result():
            print('Поздравляю, вы отгадали слово!', end='\n\n')
        else:
            print('Вы проиграли.', end='\n\n')
        game_continue = input('Если вы хотите сыграть еще раз введите "да": ').lower()
        if game_continue == 'да':
            continue
        exit()


if __name__ == '__main__':
    print('''Добро пожаловать в игру "Виселица"! 
Сейчас программа загадает слово, существительное русского языка. 
Ваша задача отгадать его прежде, чем нарисованный человек окажется на виселице. 
Вы можете играть неограниченное количество раз. Удачи!
''')
    game()


