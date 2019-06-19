from money_extractors import MoneyRangeExtractor
import pytest

# ['от 60К до 300К', '120т.р. - 160 т.р.',
#  'от 100 до 150', '$5k–$8k', 'от 2к до 4к Евро',
#  '4000-5500 $', 'Вилка :fork:: 100-250 тысяч рублей на руки', '2-4k USD', '150-250 т.р. «чистыми»',
# ''':fork::fork::fork:
# *80-90+k€*''']
cases_fork = [('от 60К до 300К грязными', '60000 RUB-300000 RUB'),
              ('от 60к до 300к gross', '60000 RUB-300000 RUB'),
              ('120т.р. - 160 т.р. чистыми', '120000 RUB-160000 RUB'),
              ('$5k–$8k', '5000 USD-8000 USD'),
              ('150-250 т.р. «чистыми»', '150000 RUB-250000 RUB'),
              ('2.5-4.5k USD', '2500.0 USD-4500.0 USD'),
              ('2.5-4.5k $', '2500.0 USD-4500.0 USD'),
              ('2.5-4.5k$', '2500.0 USD-4500.0 USD'),
              ('1K - 2K EUR нетто ', '1000 EUR-2000 EUR'),
              ('1K - 2K € нетто ', '1000 EUR-2000 EUR'),
              ('1K - 2K€ нетто ', '1000 EUR-2000 EUR'),
              ('€1K - €2K EUR нетто ', '1000 EUR-2000 EUR'),
              ('1K - 2K € нетто ', '1000 EUR-2000 EUR'),
              ('1000 - 2000 € нетто ', '1000 EUR-2000 EUR'),
              ('Оклад в вилке от 150 до 250 гросс', '150000 RUB-250000 RUB'),
              ('ЗП: 130-200к руб.', '130000 RUB-200000 RUB'),
              ('Зарплату от 200К до 1М рублей', '200000 RUB-1000000 RUB'),
              ('зп: 60 000 - 120 000 т.р. net', '60000 RUB-120000 RUB'),
              ('от 3,4 до 4,8 млн.рублей', '3400000 RUB-4800000 RUB'),
              ('280-400+ тысяч рублей', '280000 RUB-400000 RUB'),
              ('вилка $$1000-5000', '1000 USD-5000 USD'),
              ('1000-2500k USD', '1000 USD-2500 USD'),
              ('от $ 800 до 1100 net', '800 USD-1100 USD')]
cases_not_fork = ['+7(495)6386767',
                  'tel:+7(906)747-73-90',
                  '2018/01/29',
                  'Более 20 000 сотрудников по всей России',
                  'http://andrewgelman.com/2017/01/16/hiring-hiring-hiring-hiring/',
                  'Белая зп.: 150 000 рублей',
                  'График работы с 9:30 до 18:00',
                  'мы планируем вырасти с 1,5 до 50 миллионов пользователей',
                  'Equity range: 0.25-1.5%']


@pytest.fixture(scope='module')
def extractor():
    return MoneyRangeExtractor()


@pytest.mark.parametrize('test', cases_fork)
def test_fork_present(extractor, test):
    line, etalon = test
    matches = list(extractor(line))
    assert len(matches) == 1
    fact = matches[0].fact
    guess = str(fact.normalized)
    assert guess == etalon


@pytest.mark.parametrize('test', cases_not_fork)
def test_fork_not_present(extractor, test):
    line = test
    matches = list(extractor(line))
    assert len(matches) == 0


def test_fork(extractor):
    text = 'Вилка: от 60К до 300К грязными'
    matches = extractor(text).as_json
    print(matches)
    assert len(matches) != 0
    span = matches[0]['span']
    assert 'Вилка' in text[span[0]:span[1]]
