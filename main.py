import itertools
from typing import List, Tuple
import copy

from enum import IntEnum, auto

def load_wordlist(path: str) -> List[str]:
    wordlist = []
    with open(path) as f:
        line = f.readline()
        while line:
            wordlist.append(line.strip())
            line = f.readline()

    return wordlist


class Guess(IntEnum):
    GREEN = auto()
    YELLOW = auto()
    GRAY = auto()

BACKGROUND = {
    Guess.GREEN: '\033[42m',
    Guess.YELLOW: '\033[43m',
    Guess.GRAY: '\033[47m\033[30m'
}


Hint = Tuple[Guess, Guess, Guess, Guess, Guess]
ALL_HINT: List[Hint] = list(itertools.product([Guess.GREEN, Guess.YELLOW, Guess.GRAY], repeat=5))

def is_match(word: str, i_word: str, hint: Hint) -> bool:
    """word が 入力された語 (i_word) と hint に対してマッチするかどうかを返す関数
    """
    in_letters = []
    not_in_letters = []

    for i, h in enumerate(hint):
        if h == Guess.GREEN and word[i] != i_word[i]:
            return False
        elif h == Guess.YELLOW and word[i] == i_word[i]:
            return False
        elif h == Guess.YELLOW:
            in_letters.append(i_word[i])
        elif h == Guess.GRAY:
            not_in_letters.append(i_word[i])

    if all(l in word for l in in_letters) and not any(l in word for l in not_in_letters):
        return True

    return False


def candidates_from_hint(i_word: str, hint: Hint, wordlist: List[str]) -> List[str]:
    """入力された hint によって残る word たちを返す関数
    """
    candidates: List[str] = []

    for word in wordlist:
        if is_match(word, i_word, hint):
            candidates.append(word)

    return candidates


def calc_worst_hint(i_word: str, wordlist: List[str]) -> Tuple[Hint, List[str]]:
    """最悪の Hint を計算する関数
    返り値は Hint とその時に残る単語のリスト
    """
    worst_hint = ALL_HINT[0]
    max_n_cands = 0
    worst_cands = []

    for hint in ALL_HINT:
        cands = candidates_from_hint(i_word, hint, wordlist)
        if max_n_cands < len(cands):
            worst_hint = hint
            max_n_cands = len(cands)
            worst_cands = cands

    return worst_hint, worst_cands


def wordle() -> None:
    wordlist = load_wordlist('wordlist.txt')
    org_wordlist = copy.copy(wordlist)
    n_try = 0
    while n_try < 6:
        i_word = input('Input your guess > ')
        if len(i_word) != 5 or i_word not in org_wordlist:
            print('Not in word list')
            continue

        hint, wordlist = calc_worst_hint(i_word, wordlist)

        for c, h in zip(i_word, hint):
            print(f'{BACKGROUND[h]}{c}\033[0m', end='')

        print()

        if all(h == Guess.GREEN for h in hint):
            print('あなたのかち〜')
            break

        n_try += 1
    else:
        print('あなたのまけ〜')
        print(f'こたへ： {wordlist[0]}')


if __name__ == '__main__':
    wordle()
