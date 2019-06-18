import re
from itertools import chain
from typing import List, Tuple, Set
from natasha import MoneyRangeExtractor

lang_emojis = {':r:': 'r', ':python:': 'python', ':cpp:': 'c++', ':scala:': 'scala', ':java:': 'java',
               ':golang:': 'scala', ':sql:': 'sql', ':matlab:':'matlab'}
language_patterns = {'scala': 'scala', 'java': 'java', 'джав[аоуе]й?': 'java', '[cс]\+\+': 'c++',
                     'python': 'python', 'питон[ауео]?м?': 'python', '[cс]#': 'c#', 'sql': 'sql',
                     'golang': 'golang', 'matlab': 'matlab', 'матлаб[ауео]?м?': 'matlab',
                     '[\s]R[,.\s/]': 'r'}

pattern_emojis = {re.compile(pattern): normalized for pattern, normalized in lang_emojis.items()}

patterns = {re.compile(pattern, re.IGNORECASE): normalized for pattern, normalized in language_patterns.items()}


def get_languages(text: str) -> Tuple[Set[str], List[Tuple[int, int]]]:
    spans = []
    languages = set()
    for pattern, normalized in chain(pattern_emojis.items(), patterns.items()):
        x = pattern.search(text)
        if x:
            languages.add(normalized)
            spans.append((x.start(0), x.end(0)))
    return languages, spans
