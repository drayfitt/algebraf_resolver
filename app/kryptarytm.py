from app.algebraf import *


class Kryptarytm(Algebraf):
    def __init__(self, equations, words, known_letters="", url="", hints=""):
        super().__init__(url)
        self.hints = hints
        self.words = words
        self.known_letters = known_letters
        self.equations = equations

    # check equation sign and return calculation
    def kryptarytm_calculation(self, final_words, equations=""):
        if equations == "":
            equations = self.equations
        if equations == "+":
            return sum(final_words[0:-1])
        if equations == "*":
            return multiply_list(final_words[0:-1])
        if equations == "/":
            return final_words[0] / final_words[1]
        if equations == "-":
            first_word = final_words[0]
            for el in final_words[1:-1]:
                first_word -= el
            return first_word
        raise NameError("Invalid equation sign")

    # checks if known letters are in combination
    def is_in_dictionary(self, dictionary):
        check = 0
        for pair in self.known_letters:
            if pair not in dictionary.items():
                check += 1
        if check > 0:
            return False
        return True

    # checks if founded combinations fits to hints
    def is_combination_fits_hints(self, combination):
        for hint in self.hints:
            resolve_hint = replace_letters_to_numbers(combination, hint)
            elements = replace_string_type_to_int(resolve_hint[:-1])
            resolve = elements[-1]
            sign = resolve_hint[-1]
            if self.kryptarytm_calculation(elements, sign) != resolve:
                return False
        return True

    def resolve_kryptarytm(self):
        unique_letters = create_unique_letters(self.words)
        all_combinations = self.create_unique_combinations(
            unique_letters)  # format: {'h': 0, 'a': 1, 'ł': 2, 'c': 3, 'l': 4, 'm': 5, 'o': 6, 't': 7, 'u': 8, 'k': 9}
        for combination in all_combinations:
            if self.is_in_dictionary(combination):
                final_words = replace_letters_to_numbers(combination, self.words)
                if is_first_letter_zero(final_words):
                    continue
                if self.hints != "":
                    if not self.is_combination_fits_hints(combination):
                        continue
                final_words = replace_string_type_to_int(final_words)
                if self.kryptarytm_calculation(final_words) == final_words[-1]:
                    print("Success! Solution is:", final_words)
                    exit()
        print("I found nothing :(")
        exit()
