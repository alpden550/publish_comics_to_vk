# Publish comics to VK group

This script can upload comic's photo to your VK group.

Random comic is downloaded from xkcd.com

[Group example](https://vk.com/club182098076)

## How to install

You have to create VK group and create standalone VK application. After that, you must get access token via [Implicit Flow](https://vk.com/dev/implicit_flow_user)

The list of permissions must be: `scope=photos,groups,photos,wall,offline`

Create file .env in the root and write in it:

```.env
group_id=id your vk group
access_token=your access token from VK
```

Python3 must be already installed.

Should use virtual env for project isolation.

Then use `pip` (or `pip3`, if there is a conflict with Python2) to install dependencies:

```bash
pip install -r requirements.txt
```

## How to use

Run scripts in terminal

```bash
python upload_photo_to_vk.py
```

### Project Goals

The code is written for educational purposes on online-course for web-developers [dvmn.org](https://dvmn.org/).
