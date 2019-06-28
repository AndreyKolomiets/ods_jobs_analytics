import re
from itertools import chain
from typing import List, Tuple, Set
# TODO: здесь может помочь предварительная токенизация
lang_emojis = {':r:': 'r', ':python:': 'python', ':cpp:': 'c++', ':scala:': 'scala', ':java:': 'java',
               ':golang:': 'scala', ':sql:': 'sql', ':matlab:': 'matlab'}
language_patterns = {'scala': 'scala', 'java': 'java', 'джав[аоуе]й?': 'java', '[cс]\+\+': 'c++',
                     'python': 'python', 'питон[ауео]?м?': 'python', '[cс]#': 'c#', 'sql': 'sql',
                     'golang': 'golang', 'matlab': 'matlab', 'матлаб[ауео]?м?': 'matlab',
                     '[\s]R[,.\s/]': 'r', '(javascript|джаваскрипт[ауео]?м?)': 'javascript',
                     '(kotlin|котлин[ауео]?м?)': 'kotlin', 'cuda': 'cuda', 'php': 'php'}

pattern_emojis = {re.compile(pattern): normalized for pattern, normalized in lang_emojis.items()}

patterns = {re.compile(pattern, re.IGNORECASE): normalized for pattern, normalized in language_patterns.items()}

dl_frameworks = {'(py)?torch': 'pytorch',
                 '\Wtf|tensorflow': 'tensorflow', '[kK]eras': 'keras',
                 'theano': 'theano', 'mxnet': 'mxnet', 'caffe2?': 'caffe'}

bigdata = {'hadoop': 'hadoop', 'хадуп[аеоу]?м?': 'hadoop',
           '\Whive': 'hive', 'flink': 'flink',
           'spark': 'spark', 'спарк[аеоу]?м?': 'spark',
           'kafka': 'kafka', 'кафк[аоуеи]й?': 'kafka', 'airflow': 'airflow',
           'mongo': 'mongodb', 'mongodb': 'mongodb', 'монго': 'mongodb',
           '(redis|редис[аеоу]?м?)': 'redis', '(postgres|postgresql|постгрес[аеоу]?м?)': 'postgresql',
           '(clickhouse|кликхаус[аеоу]?м?)': 'clickhouse', '[ck]assandra': 'cassandra', 'hbase': 'hbase',
           'elasticsearch': 'elasticsearch', 'zeppelin': 'zeppelin'}

devops = {'(docker|докер[ауео]?м?)': 'docker', 'kubernetes': 'kubernetes'}
python_libs = {'numpy': 'numpy', 'scipy': 'scipy', 'pandas|пандас': 'pandas', '(sklearn|scikit-learn)': 'sklearn',
               'nltk': 'nltk',
               'xgboost|хгбуст': 'xgboost', 'l(ight)?gbm': 'lgbm', '(catboost|катбуст[ауео]?м?)': 'catboost',
               'opencv': 'opencv'}

all_patterns = {re.compile(pattern, re.IGNORECASE): normalized
                for pattern, normalized in chain(language_patterns.items(),
                                                 lang_emojis.items(),
                                                 dl_frameworks.items(),
                                                 bigdata.items(),
                                                 devops.items(),
                                                 python_libs.items())
                }


def get_technologies(text: str) -> Tuple[Set[str], List[Tuple[int, int]]]:
    spans = []
    languages = set()
    for pattern, normalized in all_patterns.items():
        x = pattern.search(text)
        if x:
            languages.add(normalized)
            spans.append((x.start(0), x.end(0)))
    return languages, spans
