import termcolor

import colorama
colorama.init()
colorama.deinit()

from typing import Optional

import sys

# For sentence tokenization
import nltk
nltk.download("punkt", quiet=True)

printerr = lambda x: print(x, file=sys.stderr)

from random import randint, seed
randval = lambda: randint(0, 15)

from brawndo.constants import *


def colorsafe(func):
    def wrapper(*args, **kwargs):
        colorama.reinit()
        try:
            retval = func(*args, **kwargs)
        except Exception as e:
            printerr(e)
            colorama.deinit()
            exit(1)
        colorama.deinit()
        return retval

    return wrapper


# "Function 1"
@colorsafe
def rainbow_deterministic(text: str, shift: int, testing=False) -> Optional[str]:
    test_vector = []
    for char in text:
        if char in values:
            color_value = (values[char] + shift) % 16
            color_name = colors[color_value]
            if color_name == "black":
                termcolor.cprint(char, "black", "on_white", end="")
            else:
                termcolor.cprint(char, color_name, end="")
            if testing:
                test_vector.append(f"{char},{color_name}")
        else:
            if testing:
                test_vector.append(f"{char},none")
    if testing:
        retval = "\n".join(test_vector)
        if retval[-1] != "\n":
            retval += "\n"
        return retval
    else:
        return None


# "Function 2"
@colorsafe
def word_deterministic(text: str, shift: int, testing=False) -> Optional[str]:
    wordlist = text.split(" ")
    test_vector = []
    for word in wordlist[:-1]:
        value = (sum(values[char] for char in word if char in values) + shift) % 16
        determined_color = colors[value]

        if determined_color == "black":
            colored_word = termcolor.colored(word, "black", "on_white")
        else:
            colored_word = termcolor.colored(word, determined_color)
            print(colored_word, end=" ")
        if testing:
            test_vector.append(f"{word},{determined_color}")
    value = (sum(values[char] for char in wordlist[-1] if char in values) + shift) % 16
    determined_color = colors[value]
    if determined_color == "black":
        colored_word = termcolor.colored(wordlist[-1], "black", "on_white")
    else:
        colored_word = termcolor.colored(wordlist[-1], determined_color)
    print(colored_word, end="")
    if testing:
        test_vector.append(f"{wordlist[-1]},{determined_color}")
        retval = "\n".join(test_vector)
        if retval[-1] != "\n":
            retval += "\n"
        return retval
    else:
        return None


# "Function 3"
@colorsafe
def rainbow_random(text: str, rndseed=None, testing=False) -> Optional[str]:
    test_vector = []
    if rndseed is not None and isinstance(rndseed, int):
        seed(rndseed)
    for char in text:
        random_value = randval()
        ref_color = colors[random_value]
        if ref_color == "black":
            colored_char = termcolor.colored(char, "black", "on_white")
        else:
            colored_char = termcolor.colored(char, ref_color)
        if testing:
            test_vector.append(f"{char},{ref_color}")
        print(colored_char, end="")
    if testing:
        retval = "\n".join(test_vector)
        if retval[-1] != "\n":
            retval += "\n"
        return retval
    else:
        return None


# "Function 4"
@colorsafe
def word_random(text: str, operate_on_sentences: bool, rndseed=None, testing=False) -> None:
    tokens = None
    test_vector = []
    if operate_on_sentences:
        tokens = nltk.sent_tokenize(text)
    else:
        tokens = text.split(" ")
    if rndseed is not None and isinstance(rndseed, int):
        seed(rndseed)
    for token in tokens[:-1]:
        ref_color = colors[randval()]
        if ref_color == "black":
            colored_token = termcolor.colored(token, "black", "on_white")
        else:
            colored_token = termcolor.colored(token, ref_color)
        if testing:
            test_vector.append(f"{token},{ref_color}")
        print(colored_token, end=" ")
    ref_color = colors[randval()]
    if ref_color == "black":
        colored_token = termcolor.colored(tokens[-1], "black", "on_white")
    else:
        colored_token = termcolor.colored(tokens[-1], ref_color)
    print(colored_token, end="")
    if testing:
        test_vector.append(f"{tokens[-1]},{ref_color}")
        retval = "\n".join(test_vector)
        if retval[-1] != "\n":
            retval += "\n"
        return retval
    else:
        return None
