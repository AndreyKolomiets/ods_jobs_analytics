# coding: utf-8
from __future__ import unicode_literals
import re

from yargy import (
    rule,
    and_, or_, not_
)
from yargy.interpretation import fact
from yargy.predicates import (
    gram, dictionary
)
from yargy.relations import gnc_relation

from natasha.tokenizer import TOKENIZER
from natasha.preprocess import normalize_text
from natasha.extractors import Matches
from yargy import Parser

Location = fact(
    'Location',
    ['name', 'region_or_island', 'ao_or_fo', 'federation', 'adjx_federation', 'state', 'locality', 'sea', 'island'],
)

gnc = gnc_relation()

LOCALITY = rule(
    and_(
        dictionary({
            'город',
            # 'деревня',
            # 'село',
        }),
        not_(
            or_(
                gram('Abbr'),
                gram('PREP'),
                gram('CONJ'),
                gram('PRCL'),
            ),
        ),
    ).optional(),
    and_(
        gram('ADJF'),
    ).match(gnc).optional(),
    and_(
        gram('Geox'),
        not_(
            or_(
                gram('Abbr'),
                gram('PREP'),
                gram('CONJ'),
                gram('PRCL'),
            ),
        ),
    ).match(gnc)  # .interpretation(Location.locality)
).interpretation(Location.name.inflected())

LOCATION = LOCALITY.interpretation(Location)


class Extractor(object):
    def __init__(self, r, tokenizer=TOKENIZER, tagger=None):
        self.parser = Parser(r, tokenizer=tokenizer, tagger=tagger)

    def __call__(self, text):
        text = normalize_text(text)
        matches = self.parser.findall(text)
        return Matches(text, matches)


class CustomLocationExtractor(Extractor):
    city_emojis = {':spb:': 'Санкт-Петербург',
                   ':msk:': "Москва",
                   ":default-city:": "Москва",
                   ":moscow:": "Москва",
                   ":nino_top:": "Нижний Новгород"}
    country_emoji_regex = re.compile(':flag-(\w+):')
    flags_exceptions = {'ru', 'es', 'us', 'fr', 'gb', 'de', 'uk'}

    def __init__(self):
        super(CustomLocationExtractor, self).__init__(LOCATION)

    def extract(self, message: dict):
        text = message['text']
        matches = self(text).as_json
        res = []
        for match in matches:
            if 'fact' not in match:
                continue
            start, end = match['span'][0], match['span'][1]
            # Проверяем ложные срабатывания на неденежных интервалах
            if text[start].islower():
                continue
            res.append(match)
        return res
