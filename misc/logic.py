import json
import random

with open('misc/word_rus.txt', encoding='utf8') as words_file, \
        open('misc/word_dict_rus.txt', encoding='utf8') as words_dict_file:
    all_words = set([x.strip() for x in words_file.readlines()])
    all_words_dict = json.loads(words_dict_file.read())
used_words = set()
hard_letters = {'ь', 'ъ', 'ы'}

curr_letter = None
while True:
    new_word = input()
    if new_word in used_words:
        print('Такое слово уже было, введите другое слово')
        continue
    if new_word not in all_words:
        print('Извините, я не знаю такого слова, попробуйте другое')
        continue
    if curr_letter is not None and new_word[0] != curr_letter:
        print(f'Извините, но Ваше слово должно начинаться на {curr_letter}')
        continue
    curr_letter = new_word[-1] if new_word[-1] not in hard_letters else new_word[-2]
    used_words.add(new_word)
    unused_words = all_words_dict[curr_letter]
    if not unused_words:
        print("Я не знаю слов на эту букву. Вы победили")
        break
    new_word = random.choice(unused_words)
    unused_words.remove(new_word)
    used_words.add(new_word)
    curr_letter = new_word[-1] if new_word[-1] not in hard_letters else new_word[-2]
    print(f"Мое слово: {new_word}, вам на {curr_letter}")
