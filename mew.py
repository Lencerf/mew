#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import pickle
from numpy.random import permutation

def testm2w(word_dict):
    full_score = {w:len(word_dict[w]["meanings"]) for w in word_dict}
    study_list_freq = {}  # frequency: wrodlist
    for (w, v) in word_dict.items():
        for m in v["meanings"]:
            if v["frequency"] in study_list_freq:
                study_list_freq[v["frequency"]].append(f"{m}@{w}")
            else:
                study_list_freq[v["frequency"]] = [f"{m}@{w}"]
    word_studied = set()
    for freq in sorted(study_list_freq.keys(), reverse=True):
        study_list = study_list_freq[freq]
        print(f'start frequency {freq}')
        breaked = False
        for index in permutation(len(study_list)):
            meaning, word = study_list[index].split("@", maxsplit=2)
            word_input = input(f"{meaning}: ")
            if word == word_input:
                print("Correct!")
                full_score[word] -= 1
            elif word_input == "STOP":
                breaked = True
                break
            else:
                print(f"Wrong! {meaning} <-> {word}")
            word_studied.add(word)
        if breaked:
            break
        else:
            print(f'end frequency {freq}')
    for word in word_studied:
        if full_score[word] == 0:
            if word_dict[word]["frequency"] > 0:
                word_dict[word]["frequency"] -= 1
        else:
            word_dict[word]["frequency"] += 1

def review(word_dict):
    for w in word_dict:
        print(f'{w}, frequency: {word_dict[w]["frequency"]}')
        for m in word_dict[w]["meanings"]:
            print("  ", m, end="")
        print()

def record(word_dict):
    while True:
        print("new word (imput 'STOP' to stop): ")
        text = input()
        if text == "STOP":
            print('stopped')
            print(word_dict)
            break
        else:
            text = text.split(' ')
            word = text[0]
            meanings = text[1:]
            if word in word_dict:
                word_dict[word]["frequency"] += 1
                for m in meanings:
                    word_dict[word]["meanings"].add(m)
            else:
                word_dict[word] = {
                    "frequency": 1,
                    "meanings": set(meanings)
                }

def main():
    database_file_path = sys.argv[1]
    database_file = open(database_file_path, 'rb')
    database = pickle.load(database_file)
    database_file.close()
    if len(database.keys()) > 0:
        choosed_dict = ""
        while choosed_dict not in database:  
            print("choose a dictionary:")
            for key in database.keys():
                print("  ", key)
            choosed_dict = input()
    else:
        print("create a new dictionary:")
        choosed_dict = input()
        database = {choosed_dict:{}}
    while True:
        print("what do you want to do?\n\trecord\n\treview\n\ttestM2W")
        action = input()
        if action == "exit":
            print('exiting...')
            with open(database_file_path, 'wb') as f:
                pickle.dump(database, f)
            break
        elif action == "record":
            record(database[choosed_dict])
        elif action == "testM2W":
            testm2w(database[choosed_dict])
        elif action == "review":
            review(database[choosed_dict])

if __name__ == '__main__':
    main()