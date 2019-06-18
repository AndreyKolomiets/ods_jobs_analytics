from money_extractors import MoneyRangeExtractor
# from natasha import MoneyRangeExtractor

ext = MoneyRangeExtractor()
# ['от 60К до 300К', '120т.р. - 160 т.р.',
#  'от 100 до 150', '$5k–$8k', 'от 2к до 4к Евро',
#  '4000-5500 $', 'Вилка :fork:: 100-250 тысяч рублей на руки', '2-4k USD', '150-250 т.р. «чистыми»',
# ''':fork::fork::fork:
# *80-90+k€*''']


def test_pattern1():
    text = 'от 60К до 300К грязными'
    matches = ext(text).as_json
    print(matches)
    assert len(matches) != 0
    match = matches[0]['fact']
    assert match['min']['amount'] == 60000
    assert match['min']['currency'] == 'RUB'
    assert match['max']['amount'] == 300000
    assert match['max']['currency'] == 'RUB'


def test_pattern5():
    text = 'от 60к до 300к gross'
    matches = ext(text).as_json
    print(matches)
    assert len(matches) != 0
    match = matches[0]['fact']
    assert match['min']['amount'] == 60000
    assert match['min']['currency'] == 'RUB'
    assert match['max']['amount'] == 300000
    assert match['max']['currency'] == 'RUB'


def test_pattern2():
    text = '120т.р. - 160 т.р. чистыми'
    matches = ext(text).as_json
    assert len(matches) != 0
    match = matches[0]['fact']
    assert match['min']['amount'] == 120000
    assert match['min']['currency'] == 'RUB'
    assert match['max']['amount'] == 160000
    assert match['max']['currency'] == 'RUB'
    print(matches)


def test_pattern3():
    text = '$5k–$8k'
    matches = ext(text).as_json
    assert len(matches) != 0
    match = matches[0]['fact']
    assert match['min']['amount'] == 5000
    assert match['min']['currency'] == 'USD'
    assert match['max']['amount'] == 8000
    assert match['max']['currency'] == 'USD'
    print(matches)


def test_pattern4():
    text = '150-250 т.р. «чистыми»'
    matches = ext(text).as_json
    print(matches)
    assert len(matches) != 0
    match = matches[0]['fact']
    assert match['min']['amount'] == 150000
    assert match['min']['currency'] == 'RUB'
    assert match['max']['amount'] == 250000
    assert match['max']['currency'] == 'RUB'


def test_usd():
    text = '2.5-4.5k USD'
    matches = ext(text).as_json
    print(matches)
    assert len(matches) != 0
    match = matches[0]['fact']
    assert match['min']['amount'] == 2500
    assert match['min']['currency'] == 'USD'
    assert match['max']['amount'] == 4500
    assert match['max']['currency'] == 'USD'


def test_usd2():
    text = '2.5-4.5k $'
    matches = ext(text).as_json
    print(matches)
    assert len(matches) != 0
    match = matches[0]['fact']
    assert match['min']['amount'] == 2500
    assert match['min']['currency'] == 'USD'
    assert match['max']['amount'] == 4500
    assert match['max']['currency'] == 'USD'


def test_usd3():
    text = '2.5-4.5k$'
    matches = ext(text).as_json
    print(matches)
    assert len(matches) != 0
    match = matches[0]['fact']
    assert match['min']['amount'] == 2500
    assert match['min']['currency'] == 'USD'
    assert match['max']['amount'] == 4500
    assert match['max']['currency'] == 'USD'


def test_phone():
    text = '+7(495)6386767'
    matches = ext(text)
    # assert len(matches) == 0
    assert (len(matches) == 0) or ('fact' not in matches[0])


def test_phone2():
    text = 'tel:+7(906)747-73-90'
    matches = ext(text)
    # assert len(matches) == 0
    assert (len(matches) == 0) or ('fact' not in matches[0])


def test_date():
    text = '2018/01/29'
    matches = ext(text)
    # assert len(matches) == 0
    assert (len(matches) == 0) or ('fact' not in matches[0])


def test_eur():
    text = '1K - 2K EUR нетто '
    matches = ext(text).as_json
    print(matches)
    assert len(matches) != 0
    match = matches[0]['fact']
    assert match['min']['amount'] == 1000
    assert match['min']['currency'] == 'EUR'
    assert match['max']['amount'] == 2000
    assert match['max']['currency'] == 'EUR'


def test_eur2():
    text = '1K - 2K € нетто '
    matches = ext(text).as_json
    print(matches)
    assert len(matches) != 0
    match = matches[0]['fact']
    assert match['min']['amount'] == 1000
    assert match['min']['currency'] == 'EUR'
    assert match['max']['amount'] == 2000
    assert match['max']['currency'] == 'EUR'


def test_eur3():
    text = '1K - 2K€ нетто '
    matches = ext(text).as_json
    print(matches)
    assert len(matches) != 0
    match = matches[0]['fact']
    assert match['min']['amount'] == 1000
    assert match['min']['currency'] == 'EUR'
    assert match['max']['amount'] == 2000
    assert match['max']['currency'] == 'EUR'


def test_eur4():
    text = '€1K - €2K EUR нетто '
    matches = ext(text).as_json
    print(matches)
    assert len(matches) != 0
    match = matches[0]['fact']
    assert match['min']['amount'] == 1000
    assert match['min']['currency'] == 'EUR'
    assert match['max']['amount'] == 2000
    assert match['max']['currency'] == 'EUR'


def test_eur5():
    text = '1K - 2K € нетто '
    matches = ext(text).as_json
    print(matches)
    assert len(matches) != 0
    match = matches[0]['fact']
    assert match['min']['amount'] == 1000
    assert match['min']['currency'] == 'EUR'
    assert match['max']['amount'] == 2000
    assert match['max']['currency'] == 'EUR'


def test_eur6():
    text = '1000 - 2000 € нетто '
    matches = ext(text).as_json
    print(matches)
    assert len(matches) != 0
    match = matches[0]['fact']
    assert match['min']['amount'] == 1000
    assert match['min']['currency'] == 'EUR'
    assert match['max']['amount'] == 2000
    assert match['max']['currency'] == 'EUR'


def test_fork():
    text = 'Вилка: от 60К до 300К грязными'
    matches = ext(text).as_json
    print(matches)
    assert len(matches) != 0
    span = matches[0]['span']
    assert 'Вилка' in text[span[0]:span[1]]


