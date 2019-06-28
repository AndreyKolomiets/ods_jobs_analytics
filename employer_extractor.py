import re

patterns = ['\w+\.ai',
            '([A-Za-z]+\s)+(ищет|(is)? looking for|seeks for)',
            '(компани[яию]|команд[уа]|company|стартап):? ([A-Za-z]+|\w+\.(ru|com|org|io))',
            '@\w+\.(ru|com|org|io|ai)']
# TODO: из мыла исключить общедоступные домены (gmail, yandex...)
regexes = [re.compile(_) for _ in patterns]


def extract_employer(text: str):
    spans = []
    for regex in regexes:
        for match in regex.finditer(text):
            spans.append((match.start(0), match.end(0), 'empl'))
    return spans
