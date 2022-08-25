import itertools
import urllib.request
import re
import json
import requests
from PIL import Image
from io import BytesIO
import numpy as np
import pickle


def calculate(sign, a, b):
    if sign == "+" or sign == 0:
        return a + b
    elif sign == "-" or sign == 3:
        return a - b
    elif sign == "*" or sign == 2:
        return a * b
    elif sign == "/" or sign == 1:
        return a / b
    raise NameError('Invalid sign for calculation')


def is_first_letter_zero(list_to_check):
    for e in list_to_check:
        if e[0] == '0':
            return True
    return False


# Multiply elements one by one
def multiply_list(list_to_check):
    result = 1
    for x in list_to_check:
        result = result * x
    return result


# get operations from algebraf background
def find_equations_from_background(background_image_url):
    response = requests.get(background_image_url)
    img = Image.open(BytesIO(response.content))

    # images dimensinos, what positions to crop images
    directions = [
        (208, 66, 238, 96),
        (208, 153, 238, 183),
        (208, 241, 238, 271),
        (164, 109, 194, 139),
        (341, 109, 371, 139),
        (561, 109, 591, 139)
    ]

    filename = 'model/finalized_model.sav'
    loaded_model = pickle.load(open(filename, 'rb'))

    list_of_signs = []
    # recognize equations signs and append to array
    for direction in directions:
        im = img.crop(direction).convert('RGB')
        im = np.asarray(im)
        im = im.reshape(-1, 2700)
        list_of_signs.extend(loaded_model.predict(im))

    return list_of_signs


# from words in algebraf or kryptarytm make list of unique letters
def create_unique_letters(words):
    unique_letters = set()
    for letter in words:
        unique_letters = unique_letters.union(letter)
    if len(unique_letters) != 10:
        raise NameError("Invalid number of letters! Length:", len(unique_letters), "\n", unique_letters)
    print("Unique letters:", unique_letters)
    return unique_letters


# from letters in words make numbers (type = string)
def replace_letters_to_numbers(combination, words):
    final_words = []
    for word in words:
        for sign, replacement in combination.items():
            word = word.replace(sign, str(replacement))
        final_words.append(word)
    return final_words


# from string type in array make int type
def replace_string_type_to_int(list_of_strings):
    list_of_strings = [int(x) for x in list_of_strings]
    return list_of_strings


class Algebraf:
    digits = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    def __init__(self, url):
        self.url = url

    # działanie czytane najpierw rzędami, potem kolumnami
    def find_words_and_equations(self):
        response = urllib.request.urlopen(self.url)
        html = response.read().decode('utf-8')
        # search link to algebraf background
        background_link = re.search(
            'https://d1rins9iom9m0f\.cloudfront\.net/static/img/bg/others/alg\d\d.*?\....', html)
        # from algebraf background find equations
        signs = find_equations_from_background(background_link[0])
        # search part of html where words are
        json_string = re.search('({"words":)(.*)("max_x": 17})', html)
        # reformat string to json format
        plain_json = json.loads(json_string[0])
        # if 6 position is 'h' find word on 8 position
        final_array = []
        for walk in range(0, 30):
            if plain_json['words'][walk][6] == 'h':
                if re.match('[AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuVvWwYyZzŹźŻż]+',
                            plain_json['words'][walk][8]):
                    final_array.append(re.match('[AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuVvWwYyZzŹźŻż]+',
                                                plain_json['words'][walk][8]).group(0))
        print("I found words:", final_array)
        # check if number of finded words are 9
        if len(final_array) != 9:
            raise NameError("Ups, something goes wrong! Number of words are invalid.")
        return final_array, signs  # format: ['ok', 'ikt', 'kzi', 'l', 'wl', 'amt', 'wiw', 'idw', 'ltd']

    def create_unique_combinations(self, unique_letters):
        combinations = [dict(zip(each_permutation, self.digits)) for each_permutation in
                        itertools.permutations(unique_letters, len(self.digits))]
        return combinations

    def resolve_algebraf(self):
        words, equations = self.find_words_and_equations()
        unique_letters = create_unique_letters(words)
        all_combinations = self.create_unique_combinations(unique_letters)

        for combination in all_combinations:
            final_words = replace_letters_to_numbers(combination, words)
            if is_first_letter_zero(final_words):
                continue
            final_words = replace_string_type_to_int(final_words)
            # checks if the found combination satisfies the equation
            if calculate(equations[0], final_words[0], final_words[1]) == final_words[2] \
                    and calculate(equations[1], final_words[3], final_words[4]) == final_words[5] \
                    and calculate(equations[2], final_words[6], final_words[7]) == final_words[8] \
                    and calculate(equations[3], final_words[0], final_words[3]) == final_words[6] \
                    and calculate(equations[4], final_words[1], final_words[4]) == final_words[7] \
                    and calculate(equations[5], final_words[2], final_words[5]) == final_words[8]:
                print("Success! Solution is:", final_words)
                exit()
        print("I found nothing :(")
        pass
