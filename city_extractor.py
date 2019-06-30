# coding: utf-8
from __future__ import unicode_literals
import re

from yargy import (
    rule,
    and_, or_, not_
)
from yargy.interpretation import fact
from yargy.predicates import (
    gram, dictionary, is_capitalized, eq
)
from yargy.relations import gnc_relation
from yargy.pipelines import morph_pipeline

from natasha.tokenizer import TOKENIZER
from natasha.preprocess import normalize_text
from natasha.extractors import Matches
from yargy import Parser

from typing import Set, List, Tuple
from natasha import NamesExtractor
import pandas as pd
import os
import en_core_web_sm


def get_mosmetro_stations():
    path = os.path.abspath(os.path.dirname(__file__))
    df = pd.read_csv(path+'/mosmetro.csv', encoding='utf-8')
    return df[df.Status == 'действует'].Station.values


stations = get_mosmetro_stations()

Mosmetro = fact('mosmetro', ['name'])

MOSMETRO = rule(
    or_(rule(eq('метро')),
        rule(eq('м'), eq('.'))),
    morph_pipeline(stations).interpretation(Mosmetro.name)
).interpretation(Mosmetro)

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
        is_capitalized(),
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
# TODO: мб лучше вернуть интерпретацию и возвращать только locality

LOCATION = LOCALITY.interpretation(Location)


class Extractor(object):
    def __init__(self, r, tokenizer=TOKENIZER, tagger=None):
        self.parser = Parser(r, tokenizer=tokenizer, tagger=tagger)

    def __call__(self, text):
        text = normalize_text(text)
        matches = self.parser.findall(text)
        return Matches(text, matches)


def check_location_span(name_spans: List[Tuple[int, int]], loc_span: Tuple[int, int]) -> bool:
    for span in name_spans:
        if (loc_span[0] >= span[0]) and (loc_span[1] <= span[1]):
            return True
    return False


class CustomLocationExtractor(Extractor):
    city_emojis = {'spb': 'петербург',
                   'msk': "москва",
                   "default-city": "москва",
                   "moscow": "москва",
                   "nino_top": "нижний новгород"}
    country_emoji_regex = re.compile('flag-(\w+)')
    flags_exceptions = {'ru', 'es', 'us', 'fr', 'gb', 'de', 'uk', 'belarusparrot', 'russiaparrot'}
    flags_exception_emojis = {':{}:'.format(_) for _ in flags_exceptions}
    regex_remote = re.compile('(удал[её]нная работа|работа удал[её]нная|remote job|удал[её]нка)', re.IGNORECASE)
    easy_pattern = re.compile('(?:город|city|location|локация|расположение)\s?:\s+([\w\- ]+)', re.IGNORECASE)

    def __init__(self):
        super(CustomLocationExtractor, self).__init__(LOCATION)
        self.name_ext = NamesExtractor()
        self.spacy_extractor = en_core_web_sm.load()
        self.mosmetro_ext = MosmetroExtractor()

    # TODO: пока не доделано
    def parse_emojis(self, message: dict):
        reactions = {reaction['name'] for reaction in message.get('reactions', [])}
        flag_names = []
        for name_i in reactions:
            flag_names.append(set())
            for _ in name_i:
                x = self.country_emoji_regex.search(_)
                if x:
                    flag_names[-1].add(x.group(1))
                elif _ in self.flags_exceptions:
                    flag_names[-1].add(_)

    def cities_from_emojis(self, message: dict) -> Set[str]:
        reactions = {reaction['name'] for reaction in message.get('reactions', [])}
        city_reactions = set(filter(lambda x: x in self.city_emojis, reactions))
        cities = {self.city_emojis[_] for _ in city_reactions}
        for key, value in self.city_emojis.items():
            if f':{key}:' in message['text']:
                cities.add(value)
        return cities

    def extract(self, message: dict, use_spacy=False) -> List[str]:
        text = message['text']
        x = self.easy_pattern.search(text)
        if x:
            return [x.group(1).lower()]
        matches = self(text).as_json
        name_matches = self.name_ext(text).as_json
        name_spans = [tuple(match['span']) for match in name_matches]
        res = []
        for match in matches:
            if 'fact' not in match:
                continue
            start, end = match['span'][0], match['span'][1]
            if check_location_span(name_spans, (start, end)):
                continue
            # Проверяем ложные срабатывания
            if text[start].islower():
                continue
            res.append(match['fact']['name'])

        res.extend(self.cities_from_emojis(message))
        if use_spacy:
            english_matches = [match.text for match in self.spacy_extractor(text).ents if match.label_ == 'GPE']
            res.extend(english_matches)
        if len(res) == 0:
            if self.regex_remote.search(text):
                res.append('remote')
            elif len(self.mosmetro_ext(text)) > 0:
                res.append('москва')
        return res


class MosmetroExtractor(Extractor):
    def __init__(self):
        super(MosmetroExtractor, self).__init__(MOSMETRO)
