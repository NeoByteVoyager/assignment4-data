from curses.ascii import isalpha

import nltk
from nltk.tokenize import word_tokenize


def gopher_quality_filter(text: str) -> bool:
    ''''
    remove contents:
        Contain less than 50 or more than 100,000 words.
        Have a mean word length outside the range of 3 to 10 characters.
        Have more than 30% of lines ending with an ellipsis (“...”).
        Contain less than 80% of words with at least one alphabetic character.
    '''
    words = word_tokenize(text)
    word_num = len(words)
    # rule 1
    if word_num < 50 or word_num > 100000:
        return False
    # rule 2
    total_length = 0
    for word in words:
        total_length += len(word)

    avg_length = total_length / word_num
    if avg_length < 3 or avg_length > 10:
        return False
    # rule 3
    lines = text.splitlines()

    ellipsis_lines = 0
    for line in lines:
        if line.strip()[-3:] == '...':
            ellipsis_lines += 1

    if ellipsis_lines / len(lines) > 0.3:
        return False

    # rule 4
    has_alpha_num = 0
    for word in words:
        for c in word:
            if c.isalpha():
                has_alpha_num += 1
                break
    return has_alpha_num / word_num >= 0.8


if __name__ == "__main__":
    print(gopher_quality_filter("hello this beautiful girl, i want to play with you"))