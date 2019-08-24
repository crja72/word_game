import json
import random

from flask import Flask, request

with open('misc/singular.txt', encoding='utf8') as words_file, \
        open('misc/singular_dict_rus.txt', encoding='utf8') as words_dict_file:
    ALL_WORDS = set([x.strip() for x in words_file.readlines()])
    ALL_WORDS_DICT = json.loads(words_dict_file.read())

HARD_LETTERS = {'ь', 'ъ', 'ы'}

app = Flask(__name__)
session_storage = {}


def start_new_game():
    return {
        'all_words': ALL_WORDS,
        'unused_words_dict': ALL_WORDS_DICT.copy(),
        'used_words': set(),
        'cur_letter': None
    }


@app.route('/post', methods=['POST'])
def main():
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    handle_dialog(request.json, response)
    response['response']['tts'] = response['response']['text']
    return json.dumps(response)


def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        session_storage[user_id] = start_new_game()
        res['response']['text'] = """Привет! Давай играть в слова. Скажи первое слово. 
        Это должно быть существительное в именительном падеже. Если хотите играть сначала, скажите 'сначала', если
        сдаетесь, то 'сдаюсь'"""
        return

    new_word = req['request']['original_utterance'].lower()
    if new_word == 'сдаюсь':
        res['response']['text'] = 'Машина победила. Уа-ха-ха'
        res['response']['end_session'] = True
        return
    if new_word == 'сначала':
        res['response']['text'] = 'Начнем сначала, скажите первое слово'
        session_storage[user_id] = start_new_game()
        return
    if new_word in session_storage[user_id]['used_words']:
        res['response']['text'] = 'Такое слово уже было, введите другое слово'
        return
    if new_word not in session_storage[user_id]['all_words']:
        res['response']['text'] = 'Извините, я не знаю такого слова, попробуйте другое'
        return
    curr_letter = session_storage[user_id]['cur_letter']
    if curr_letter is not None and new_word[0] != curr_letter:
        res['response']['text'] = f"Извините, но Ваше слово должно начинаться на {curr_letter}"
        return
    curr_letter = new_word[-1] if new_word[-1] not in HARD_LETTERS else new_word[-2]
    session_storage[user_id]['used_words'].add(new_word)
    unused_words = session_storage[user_id]['unused_words_dict'][curr_letter]
    if not unused_words:
        res['response']['text'] = "Я больше не знаю слов на эту букву. Вы победили"
        res['response']['end_session'] = True
        return
    new_word = random.choice(unused_words)
    unused_words.remove(new_word)
    session_storage[user_id]['used_words'].add(new_word)
    session_storage[user_id]['cur_letter'] = new_word[-1] if new_word[-1] not in HARD_LETTERS else new_word[-2]
    res['response']['text'] = f"Мое слово: {new_word}, вам на {session_storage[user_id]['cur_letter']}"


if __name__ == '__main__':
    app.run()
