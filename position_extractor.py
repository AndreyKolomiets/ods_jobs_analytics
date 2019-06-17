import re

from yargy import (
    rule,
    and_, or_,
)
from yargy.interpretation import (
    fact,
    const,
    attribute
)
from yargy.predicates import (
    eq, length_eq,
    in_, in_caseless,
    gram, type,
    normalized, caseless, dictionary
)
from yargy.pipelines import morph_pipeline, caseless_pipeline

from natasha.utils import Record

from natasha.extractors import Extractor

from natasha.dsl import (
    Normalizable,
    money as dsl
)

Position = fact('position', ['level', 'field', 'name'])

LEVEL = rule(caseless_pipeline(['junior', 'middle', 'senior', 'lead', 'chief']).interpretation(Position.level))

# TODO: тут нужен or_, чтобы писать DS и DE только большими буквами
NAME = rule(caseless_pipeline(['data scientist', 'data engineer',
                               'ds', 'de', 'engineer',
                               'analyst', 'data analyst', 'bi analyst',
                               'data manager']).interpretation(Position.name))

FIELD = rule(caseless_pipeline(['ML', 'DL', 'CV', 'NLP',
                                'machine learning', 'deep learning']).interpretation(Position.field))

POSITION = rule(LEVEL.optional(),
                FIELD.optional(),
                NAME).interpretation(Position)


class PositionExtractor(Extractor):
    def __init__(self):
        super(PositionExtractor, self).__init__(POSITION)

