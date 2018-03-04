#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import yaml
from numpy.random import permutation
from general_codes.utils import sayFinished

def red_text(text):
    return f'\033[31m {text}\033[00m'
def green_text(text):
    return f'\033[32m {text}\033[00m'
def bold_text(text):
    return f"\033[1m{text}\033[0m"

def save_exit(database, word_to_learn):
    print('exiting...')
    for word_at_list, items in word_to_learn.items():
        word, list_name = word_at_list.split("@", 1)
        database[list_name][word] = items
    with open(sys.argv[1], 'w', encoding='utf-8') as f:
        yaml.dump(database, f, allow_unicode=True)
    exit(0)

def review(database, word_to_learn):
    word_to_learn_array = [(word_at_list, items) 
        for word_at_list, items in word_to_learn.items()]
    word_to_learn_array.sort(key=lambda w:(w[1]["f"], w[1]['h']), reverse=True)
    for word_at_list, items in word_to_learn_array:
        word = word_at_list.split("@", 1)[0]
        print(f'{word}, frequency: {items["f"]}, h:{items["h"]}')
        for m in items["m"]:
            print("  ", m, end="")
        sayFinished(word)
        if input('  ') == '':
            continue
        else:
            break

def dictation(database, word_to_learn):
    test_word(database, word_to_learn, say_meaning=True)

def test_word(database, word_to_learn, say_meaning=False):
    full_score = {w:0 for w in word_to_learn}
    study_list_freq = {}  # {frequency:{h:wordlist}}
    for w, v in word_to_learn.items():
        for m in v["m"]:
            if v['f'] not in study_list_freq:
                study_list_freq[v['f']] = {}
            if v['h'] not in study_list_freq[v["f"]]:
                study_list_freq[v["f"]][v['h']] = []
            study_list_freq[v["f"]][v['h']].append(f"{m}@{w}")
    word_studied = set()
    for freq in sorted(study_list_freq.keys(), reverse=True):
        print(bold_text(f'start frequency {freq}'))
        broken = False
        for historical_h in sorted(study_list_freq[freq].keys(), reverse=True):    
            study_list = study_list_freq[freq][historical_h]
            for index in permutation(len(study_list)):
                meaning, word, at_list = study_list[index].split("@", maxsplit=2)
                if say_meaning:
                    sayFinished(meaning)
                else:
                    print(f"{meaning}: ", end='')
                word_input = input()
                if word == word_input:
                    print(green_text("Correct!"), f"h={historical_h}")
                elif word_input == "STOP":
                    broken = True
                    current_word_at_list = f"{word}@{at_list}"
                    if current_word_at_list in word_studied and full_score[current_word_at_list] == 0:
                        word_studied.remove(current_word_at_list)
                    break
                else:
                    full_score[f"{word}@{at_list}"] -= 1
                    print(f"{red_text('Wrong!')} {meaning} <-> {word}")
                word_studied.add(f"{word}@{at_list}")
            if broken:
                break
        if broken:
            break
        else:
            print(bold_text(f'end frequency {freq}'))
    for word in word_studied:
        #print(full_score[word])
        if full_score[word] == 0:
            if word_to_learn[word]['f'] > 0:
                word_to_learn[word]['f'] -= 1
        else:
            word_to_learn[word]['f'] += 1
            word_to_learn[word]['h'] += 1

FUNCTION_TABLE = [
    {
        "name": "review",
        "func": review
    },{
        "name": "exit",
        "func": save_exit
    },{
        "name": "test",
        "func": test_word
    } 
]

def main():
    database_file_path = sys.argv[1]
    database_file = open(database_file_path, 'r')
    database = yaml.load(database_file)
    database_file.close()
    if len(database.keys()) > 0:
        print("choose a dictionary or type in a new dictionary name:")
        for key in database.keys():
            print("\t", key)
        chosen_dict_name = input()
        if chosen_dict_name not in database and chosen_dict_name != "ALL":  
            database[chosen_dict_name] = {}
            print(f'new dictionary {chosen_dict_name} created.')
    else:
        print("create a new dictionary:")
        chosen_dict_name = input()
        database = {chosen_dict_name:{}}
        print(f'new dictionary {chosen_dict_name} created.')
    word_to_learn = {}
    if chosen_dict_name != 'ALL':
        for word, items in database[chosen_dict_name].items():
            word_to_learn[f'{word}@{chosen_dict_name}'] = items
    else:
        for list_name, list_content in database.items():
            for word, items in list_content.items():
                word_to_learn[f'{word}@{list_name}'] = items
    while True:
        print("what do you want to do?")
        function_names = [f['name'] for f in FUNCTION_TABLE]
        for index, function in enumerate(FUNCTION_TABLE):
            print(f'\t{index}:',  function['name'])
        input_text = input()
        chosen_func_index = None
        if input_text in function_names:
            chosen_func_index = function_names.index(input_text)
        else:
            chosen_func_index = int(input_text)
        if chosen_func_index < len(FUNCTION_TABLE):
            FUNCTION_TABLE[chosen_func_index]['func'](database, word_to_learn)
    

if __name__ == '__main__':
    main()