import argparse
import json
from tqdm.auto import tqdm
from extractors.money_extractors import MoneyRangeExtractor
from extractors.technology_extractor import get_technologies
from extractors.position_extractor import PositionExtractor

parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, help='Путь к json с постами')
args = parser.parse_args()

with open(args.path, 'r', encoding='utf-8') as f:
    data = json.load(f)
job_posts = data['job_posts']

money_ext = MoneyRangeExtractor()
pos_ext = PositionExtractor()
for message in tqdm(job_posts):
    forks = [money_ext.extract(message['text']) for message in tqdm(job_posts)]
    technologies = [get_technologies(message['text']) for message in tqdm(job_posts)]

