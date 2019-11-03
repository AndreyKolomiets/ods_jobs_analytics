from city_extractor import CustomLocationExtractor, MosmetroExtractor
import pytest


cases_city = [('Москва', 'москва'),
              ("Локация: Берлин", "берлин"),
              ("Офис расположен в Минске", "минск"),
              ("Офис - в лучшем городе Земли :msk:", 'москва'),
              ({'text': 'Вакансия: Junior Data Scientist', 'reactions': [{'name': 'default-city'}]}, 'москва'),
              ('Мы находимся в городе Таганрог', "таганрог"),
              ("офис находится в Таганроге", "таганрог"),
              ("Вакансия: data scientist (stealth mode startup в области real estate), удаленная работа", "remote"),
              ("Работа в офисе в Москве или удаленка", "москва"),
              ('Location: New York', 'New York'),
              ("офис расположен на м. Парк Культуры", "москва"),
              ('- Офис на ст.м. Кропоткинская', 'москва')
              ]

cases_not_city = ['кампания',
                  "у нее красивые глаза",
                  "мирный город",
                  "контактное лицо - Артем Грачев",
                  "по указу президента Владимира Путина",
                  'Контактное лицо - Виктория Иванова',
                  'echo.msk.ru',
                  "Разработка программного обеспечения"]

cases_metro = [('офис расположен на м. Арбатская', 'Арбатская'),
               ('расположение: метро Парк Культуры', 'Парк Культуры')]


@pytest.fixture(scope='module')
def metro_extractor():
    return MosmetroExtractor()


@pytest.mark.parametrize('test', cases_metro)
def test_mosmetro(metro_extractor, test):
    line, etalon = test
    matches = metro_extractor(line)
    assert len(matches) == 1
    assert matches[0].fact.name == etalon


@pytest.fixture(scope='module')
def extractor():
    return CustomLocationExtractor()


@pytest.mark.parametrize('test', cases_city)
def test_city(extractor, test):
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

