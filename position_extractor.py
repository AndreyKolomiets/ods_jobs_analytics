from yargy import (
    rule, or_
)
from yargy.interpretation import (
    fact
)
from yargy.predicates import (
    dictionary, is_capitalized, eq, caseless
)
from yargy.pipelines import caseless_pipeline, morph_pipeline

from natasha.extractors import Extractor

Position = fact('position', ['level', 'field', 'name'])

LEVEL = rule(caseless_pipeline(['junior', 'middle', 'senior',
                                'lead', 'chief', 'head', 'team lead',
                                "старший", "младший",
                                "руководитель направления"]).interpretation(Position.level))

# TODO: нужно учесть жаргонные варианты (датасаентолог, датасатанист и т.д.) Скорее всего, придется парсить регулярками
NAME = rule(or_(caseless_pipeline(['data scientist', 'data engineer', 'engineer',
                                   'analyst', 'data analyst',
                                   'data manager', 'scientist', 'researcher',
                                   "developer",
                                   "intern"]),
                rule(dictionary(['DS', 'DE']), is_capitalized()),
                morph_pipeline(["аналитик", "разработчик", "стажер"])).interpretation(Position.name.inflected()))

FIELD = rule(caseless_pipeline(['ML', 'DL', 'CV', 'computer vision', 'NLP', 'bi',
                                'machine learning', 'deep learning',
                                'software', 'research', 'big data',
                                'python', 'c++', "scala", "java",
                                'ios', "android", 'devops',
                                "backend", 'frontend']).interpretation(Position.field))

HEAD = rule(caseless('head').interpretation(Position.level),
            eq('of'),
            caseless_pipeline(['analytics', 'predictive analytics', 'data science']).interpretation(Position.field))

POSITION = or_(rule(LEVEL.optional(),
                    FIELD.optional(),
                    eq('-').optional(),
                    NAME),
               HEAD).interpretation(Position)


# TODO: нужен метод extract с фильтрацией. Например, разбирать возможные ложные срабатывания ("аналитика"),
#  фильтровать по длине (чем больше полей заполнено, тем предпочтительнее)
#  можно выдавать "аналитик" только тогда, когда ничего более конкретного не нашлось
class PositionExtractor(Extractor):
    def __init__(self):
        super(PositionExtractor, self).__init__(POSITION)
