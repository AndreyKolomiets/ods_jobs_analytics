from position_extractor import PositionExtractor

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
