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
    normalized, caseless, dictionary, is_capitalized
)
from yargy.pipelines import morph_pipeline, caseless_pipeline

from natasha.utils import Record

from natasha.extractors import Extractor

from natasha.dsl import (
    Normalizable,
    money as dsl
)

Position = fact('position', ['level', 'field', 'name'])

LEVEL = rule(caseless_pipeline(['junior', 'middle', 'senior', 'lead', 'chief', 'head']).interpretation(Position.level))

# TODO: нужно учесть head of (analytics, data science...)
NAME = rule(or_(caseless_pipeline(['data scientist', 'data engineer', 'engineer',
                               'analyst', 'data analyst',
                               'data manager']),
                rule(dictionary(['DS', 'DE']), is_capitalized())).interpretation(Position.name))

FIELD = rule(caseless_pipeline(['ML', 'DL', 'CV', 'computer vision', 'NLP', 'bi',
                                'machine learning', 'deep learning']).interpretation(Position.field))

POSITION = rule(LEVEL.optional(),
                FIELD.optional(),
                NAME).interpretation(Position)


class PositionExtractor(Extractor):
    def __init__(self):
        super(PositionExtractor, self).__init__(POSITION)

