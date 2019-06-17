from money_extractors import MoneyRangeExtractor


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


if __name__ == '__main__':
    test_pattern5()
    test_pattern1()
    test_pattern2()
    test_pattern4()
    test_pattern3()

