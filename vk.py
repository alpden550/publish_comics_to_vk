import os
import requests
from dotenv import load_dotenv
import download_comics


load_dotenv()
VK_URL = 'https://api.vk.com/method/{}'
API_VERSION = 5.95
ACCESS_TOKEN = os.getenv('access_token')
GROUP_ID = 182098076


def get_url_from_upload_photo(group_id):
    url = VK_URL.format('photos.getWallUploadServer')
    parameters = {
        'access_token': ACCESS_TOKEN,
        'v': API_VERSION,
    }
    response = requests.get(url, params=parameters)
    if response.ok:
        return response.json().get('response').get('upload_url')


def upload_photo(upload_url, photo):
    with open(photo, 'rb') as image:
        files = {
            'photo': image,
        }
        response = requests.post(upload_url, files=files)
        return response.json()


def save_wall_photo(photo_data, group_id):
    url = VK_URL.format('photos.saveWallPhoto')
    parameters = {
        'access_token': ACCESS_TOKEN,
        'v': API_VERSION,
        'photo': photo_data.get('photo'),
        'server': photo_data.get('server'),
        'hash': photo_data.get('hash'),
    }
    response = requests.post(url, data=parameters).json().get('response')[0]
    owner_id, media_id = response.get('owner_id'), response.get('id')
    return owner_id, media_id


def wall_post(photo_data, group_id, message):
    photo_owner_id, media_id = photo_data
    url = VK_URL.format('wall.post')
    parameters = {
        'access_token': ACCESS_TOKEN,
        'v': API_VERSION,
        'owner_id': -group_id,
        'from_group': 1,
        'message': message,
        'attachments': f'photo{photo_owner_id}_{media_id}',
    }
    requests.post(url, data=parameters)


if __name__ == "__main__":
    comic = download_comics.get_latest_comic()
    comic_image = download_comics.download_comic_image(comic)
    comic_name = download_comics.get_filename(comic.get('img'))
    comic_description = download_comics.get_comic_description(comic)

    upload_url = get_url_from_upload_photo(group_id=GROUP_ID)
    photo_raw_data = upload_photo(upload_url, photo=f'comics/{comic_name}')
    photo_id = save_wall_photo(photo_data=photo_raw_data,
                               group_id=GROUP_ID)
    wall_post(photo_data=photo_id,
              group_id=GROUP_ID,
              message=comic_description)
