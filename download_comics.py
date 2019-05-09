from urllib.parse import urlparse
import os
import random
import requests


LATEST_COMIC = 'https://xkcd.com/info.0.json'


def get_filename(file):
    path = urlparse(file)
    return path.path.split('/')[-1]


def get_latest_comic(url=LATEST_COMIC):
    response = requests.get(url)
    if response.ok:
        return response.json().get('num')


def get_random_comic(comic_number=1):
    random_comic = random.randint(1, comic_number)
    url = f'http://xkcd.com/{random_comic}/info.0.json'
    response = requests.get(url)
    if response.ok:
        return response.json()


def download_comic_image(comic_data):
    os.makedirs('comics', exist_ok=True)

    image_url = comic_data.get('img')
    image_name = get_filename(image_url)
    response = requests.get(image_url)
    if not response.ok:
        return None

    with open(f'comics/{image_name}', 'wb') as file:
        file.write(response.content)


def get_comic_description(comic_data):
    return comic_data.get('alt')


if __name__ == "__main__":
    latest_comic = get_latest_comic()
    random_comic = get_random_comic(latest_comic)

    image = download_comic_image(random_comic)
