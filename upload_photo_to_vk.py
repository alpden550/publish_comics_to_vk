import os
import requests
from dotenv import load_dotenv
import download_comics


load_dotenv()
VK_URL = 'https://api.vk.com/method/{}'
API_VERSION = 5.95
ACCESS_TOKEN = os.getenv('access_token')
GROUP_ID = -int(os.getenv('group_id'))


def put_to_vk(method, **kwargs):
    url = VK_URL.format(method)
    parameters = {
        'access_token': ACCESS_TOKEN,
        'v': API_VERSION,
    }
    parameters.update(kwargs)
    response = requests.post(url, data=parameters).json()

    if 'error' in response:
        raise requests.HTTPError(response['error'])

    return response


def get_url_from_upload_photo():
    url = VK_URL.format('photos.getWallUploadServer')
    parameters = {
        'access_token': ACCESS_TOKEN,
        'v': API_VERSION,
    }
    response = requests.get(url, params=parameters).json()
    if 'error' in response:
        raise requests.HTTPError(response['error'])
    return response.get('response').get('upload_url')


def upload_photo(upload_url, photo):
    with open(photo, 'rb') as image:
        files = {
            'photo': image,
        }
        return requests.post(upload_url, files=files).json()


def save_wall_photo(photo_data, method='photos.saveWallPhoto'):
    vk_photo = photo_data.get('photo')
    vk_server = photo_data.get('server')
    vk_hash = photo_data.get('hash')
    try:
        response = put_to_vk(method, photo=vk_photo, server=vk_server, hash=vk_hash)
        photo_data = response.get('response')[0]
        owner_id, media_id = photo_data.get('owner_id'), photo_data.get('id')
    except requests.HTTPError:
        owner_id, media_id = None, None

    return owner_id, media_id


def wall_post(photo_data, group_id, message, method='wall.post'):
    photo_owner_id, media_id = photo_data

    put_to_vk('wall.post',
              owner_id=group_id,
              from_group=-1,
              message=message,
              attachments=f'photo{photo_owner_id}_{media_id}')


if __name__ == "__main__":
    latest_comic = download_comics.get_latest_comic()
    random_comic = download_comics.get_random_comic(latest_comic)
    comic_image = download_comics.download_comic_image(random_comic)
    comic_name = download_comics.get_filename(random_comic.get('img'))
    comic_description = download_comics.get_comic_description(random_comic)

    try:
        upload_url = get_url_from_upload_photo()
    except requests.HTTPError:
        upload_url = None

    try:
        photo_raw_data = upload_photo(upload_url, photo=f'comics/{comic_name}')
    except FileNotFoundError:
        photo_raw_data = None
    if photo_raw_data is not None:
        photo_id = save_wall_photo(photo_data=photo_raw_data)
        wall_post(photo_data=photo_id,
                  group_id=GROUP_ID,
                  message=comic_description)

    os.remove(f'comics/{comic_name}')
