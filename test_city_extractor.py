from city_extractor import CustomLocationExtractor
import pytest


cases_city = [('Москва', 'москва'),
              ("Локация: Берлин", "берлин"),
              ("Офис расположен в Минске", "минск"),
              ("Офис - в лучшем городе Земли :msk:", 'москва'),
              ({'text': 'Вакансия: Junior Data Scientist', 'reactions': [{'name': 'default-city'}]}, 'москва')]
cases_not_city = ['кампания',
                  "у нее красивые глаза",
                  "мирный город",
                  "контактное лицо - Артем Грачев",
                  "по указу президента Владимира Путина",
                  'Контактное лицо - Виктория Иванова',
                  'echo.msk.ru']


@pytest.fixture(scope='module')
def extractor():
    return CustomLocationExtractor()


@pytest.mark.parametrize('test', cases_city)
def test_fork_present(extractor, test):
    line, etalon = test
    # matches = list(extractor(line))
    if isinstance(line, str):
        matches = extractor.extract({'text': line})
    else:
        matches = extractor.extract(line)
    assert len(matches) == 1
    # assert matches[0].fact.name == etalon
    assert matches[0] == etalon


@pytest.mark.parametrize('test', cases_not_city)
def test_not_city(extractor, test):
    line = test
    # matches = list(extractor(line))
    matches = extractor.extract({'text': line})
    assert len(matches) == 0

