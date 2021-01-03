#!/usr/bin/env python
# -*- coding: utf-8 -*-

def hamming_distance(string1, string2):
    return sum(wordString1 != wordString2 for wordString1, wordString2 in zip(string1, string2))

def optimist_distance(string1, string2):
    return hamming_distance(string1, string2) + abs(len(string1) - len(string2))

def optimist_levenshtein(string1, string2):
    vocab = set(string1)
    vocab.update(set(string2))

    result = {
        -1: 0,
        1: 0
    }
    for letter in vocab:
        difference = string1.count(letter) - string2.count(letter)
        if difference < 0:
            result[-1] += abs(difference)
        else:
            result[1] += difference

    return max(result[-1], result[1])
