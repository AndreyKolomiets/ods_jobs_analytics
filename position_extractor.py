from yargy import (
    rule, or_,
)
from yargy.interpretation import (
    fact
)
from yargy.predicates import (
    dictionary, is_capitalized
)
from yargy.pipelines import caseless_pipeline

from natasha.extractors import Extractor

Position = fact('position', ['level', 'field', 'name'])

LEVEL = rule(caseless_pipeline(['junior', 'middle', 'senior', 'lead', 'chief', 'head']).interpretation(Position.level))

# TODO: нужно учесть head of (analytics, data science...)
NAME = rule(or_(caseless_pipeline(['data scientist', 'data engineer', 'engineer',
                                   'analyst', 'data analyst',
                                   'data manager', 'scientist']),
                rule(dictionary(['DS', 'DE']), is_capitalized())).interpretation(Position.name))

FIELD = rule(caseless_pipeline(['ML', 'DL', 'CV', 'computer vision', 'NLP', 'bi',
                                'machine learning', 'deep learning',
                                'software', 'research']).interpretation(Position.field))

POSITION = rule(LEVEL.optional(),
                FIELD.optional(),
                NAME).interpretation(Position)


class PositionExtractor(Extractor):
    def __init__(self):
        super(PositionExtractor, self).__init__(POSITION)
