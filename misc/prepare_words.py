import json

with open("singular.txt", encoding="utf8") as fin:
    words_li = [x.strip() for x in fin.readlines()]
words_di = {}
for word in words_li:
    if word[0] in words_di:
        words_di[word[0]].append(word)
    else:
        words_di[word[0]] = [word]
with open("singular_dict_rus.txt", mode='w', encoding='utf8') as fout:
    fout.write(json.dumps(words_di, ensure_ascii=False, indent=4))
