from extractors.position_extractor import PositionExtractor

ext = PositionExtractor()


def test_ds():
    matches = ext('Data scientist').as_json
    assert len(matches) > 0
    match = matches[0]
    assert match['fact']['name'].lower() == 'data scientist'


def test_ml_engineer():
    matches = ext('Machine learning engineer').as_json
    assert len(matches) > 0
    match = matches[0]
    assert match['fact']['name'].lower() == 'engineer'
    assert match['fact']['field'].lower() == 'machine learning'


def test_de():
    text = 'flag-de'
    matches = ext(text).as_json
    assert len(matches) == 0


def test_head():
    matches = ext('Head of data science').as_json
    assert len(matches) > 0
    match = matches[0]
    assert match['fact']['level'].lower() == 'head'
    assert match['fact']['field'].lower() == 'data science'


def test_head_ru():
    text = 'ищет Руководителя направления скоринга'
    matches = ext(text).as_json
    assert len(matches) > 0
    match = matches[0]
    assert match['fact']['level'].lower() == 'руководитель направления'


def test_dashed():
    text = ' ищем senior python-разработчика'
    matches = ext(text).as_json
    assert len(matches) > 0
    match = matches[0]
    assert match['fact']['level'].lower() == 'senior'
    assert match['fact']['field'].lower() == 'python'
    assert match['fact']['name'].lower() == 'разработчик'


def test_cpp():
    text = ' разыскивается senior c++ developer'
    matches = ext(text).as_json
    assert len(matches) > 0
    match = matches[0]
    assert match['fact']['level'].lower() == 'senior'
    assert match['fact']['field'].lower() == 'c++'
    assert match['fact']['name'].lower() == 'developer'
