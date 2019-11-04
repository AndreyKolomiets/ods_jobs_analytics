import argparse
from tqdm import tqdm
import json
import glob
from typing import List, Tuple, Dict

# Каналы, сообщения из которых извлекаются
CHANNELS = (
    '_jobs',
    '_jobs_hr',
    '_top_jobs'
)
# Поскольку раньше в jobs не использовались треды, то нужно игнорировать заглавные посты, не являющиеся вакансиями.
# Самые популярные паттерны ниже
PATTERNS_TO_IGNORE = (
    'This message was deleted.',
    'has joined the channel',
    'has left the channel'
)


def main(root: str,
         min_year: int) -> Tuple[List[Dict], List[Dict]]:
    """
    Извлечение постов с вакансиями
    :param root:
    :param min_year:
    :return: список постов с вакансиями, список постов с дайджестами вакансий из #_top_jobs
    """
    job_posts = []
    top_jobs = []

    for name in tqdm(list(glob.iglob(root + "/*/*.json"))):

        channel, date = name.split('/')[-2:]

        if channel not in CHANNELS:
            continue

        date = date.rstrip('.json')
        year, month, day = date.split('-')
        if int(year) < min_year:
            continue

        with open(name) as msgs_file:
            messages = json.load(msgs_file)

        for message in messages:
            # Учитываем только заглавные посты (вакансии в тредах почти не встречаются)
            if ('thread_ts' not in message) or (message['thread_ts'] == message['ts']):
                if all(pattern not in message['text'] for pattern in PATTERNS_TO_IGNORE):
                    if channel == '_top_jobs':
                        top_jobs.append(message)
                    else:
                        job_posts.append(message)
    return job_posts, top_jobs


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=str, help='Путь к распакованному дампу слака')
    parser.add_argument('--min_year', type=int, help='Минимальный год, для которого смотрим вакансии')

    args = parser.parse_args()
    jobs, top_jobs = main(args.root, args.min_year)
    print(f'Извлечено {len(jobs)} вакансий, {len(top_jobs)} постов из top_jobs')
    with open('jobs.json', 'w') as f:
        json.dump({'job_posts': jobs, 'top_jobs': top_jobs}, f)
