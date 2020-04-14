"""
How to Prove My Worth

My name is Alain Sánchez Gutiérrez. I'm a Software Developer and Father, both at full time. I like self-learn and I learn quick. I enjoy teach what I learn. I believe in teamwork and help teammates when they need.

This exam was developed on Windows 10 with Python 3.6 using PyCharm 2020.1.

Please read README.md file before do anything
"""
import os

import requests
from PIL import Image, ImageDraw, ImageFont
from bs4 import BeautifulSoup
from dotenv import load_dotenv


def watermark_text(input_image_path,
                   output_image_path,
                   text, pos=None):
    photo = Image.open(os.path.join(str(BASE_DIR), input_image_path))
    drawing = ImageDraw.Draw(photo)
    color = (255, 69, 0)
    font = ImageFont.truetype(os.path.join(str(BASE_DIR), 'fonts', 'FreeMono.ttf'), size=20)
    pos = pos if pos else (photo.width / 4, photo.height / 2)
    drawing.text(pos, text, fill=color, font=font)
    photo.show()
    photo.save(os.path.join(str(BASE_DIR), output_image_path))


def save_file(content, filename, mode='w'):
    with open(filename, mode) as file:
        file.write(content)
        file.close()


def main():
    the_name = os.getenv('FULL_NAME')
    the_username = os.getenv('USERNAME')
    the_email = os.getenv('EMAIL')
    the_cv = os.getenv('CV')
    the_aboutme = os.getenv('ABOUT_ME')
    the_code = os.getenv('CODE')

    session = requests.Session()

    start_url = 'https://www.proveyourworth.net/level3/start'
    start_page = session.get(url=start_url)
    print('*** Start ***')
    print(f'STATUS: {start_page.status_code}')

    soup = BeautifulSoup(start_page.content, 'html.parser')
    stateful_hash = soup.find('input', {'name': 'statefulhash'}).get('value')

    activate_url = f'https://www.proveyourworth.net/level3/activate?statefulhash={stateful_hash}&username={the_username}'
    activate_page = session.get(url=activate_url)
    print('\n*** Activate ***')
    print(f'STATUS: {activate_page.status_code}')

    payload_url = activate_page.headers.get('X-Payload-URL')
    if not payload_url:
        print('\nInvalid. No payload url. Try again.')
        exit()

    payload_page = session.get(url=payload_url, stream=True)
    print('\n*** Payload ***')
    print(f'STATUS: {payload_page.status_code}')

    payload_filename = payload_page.headers.get('Content-Disposition').split('filename=')[1]
    if not payload_filename:
        print('\nInvalid. No payload url. Try again.')
        exit()

    save_file(content=payload_page.content, filename=payload_filename, mode='wb')

    if not {'X-Post-Back-To', 'X-Post-Back-Fields', 'X-Please-Also-Provide', 'X-By-The-Way'} <= set(dict(payload_page.headers).keys()):
        print('\nInvalid payload headers. Try again.')
        exit()

    post_back_url = payload_page.headers.get('X-Post-Back-To')

    payload_file = payload_filename.split('.')
    payload_filename_with_sign = payload_file[0] + '_with_sign.' + payload_file[1]
    watermark_text(payload_filename, payload_filename_with_sign,
                   text=f'{the_name}\nHash: {stateful_hash}',
                   pos=(192, 128))

    with open(os.path.join(str(BASE_DIR), the_cv), 'rb') as resume_file, \
            open(os.path.join(str(BASE_DIR), payload_filename_with_sign), 'rb') as image_file_signed, \
            open(os.path.join(str(BASE_DIR), the_code), 'rb') as code_file:
        post_data = {'name': the_name, 'email': the_email, 'aboutme': the_aboutme}
        post_files = {'resume': resume_file, 'code': code_file, 'image': image_file_signed}
        post_back_page = session.post(post_back_url, data=post_data, files=post_files)
        print('\n*** Post Back ***')
        print(f'STATUS: {post_back_page.status_code}')


if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    if not os.path.exists(os.path.join(str(BASE_DIR), '.env')):
        print('\nInvalid. No ".env" file detected. Please read topic "Create and update environment values" in README.md file')
        exit()

    load_dotenv(dotenv_path=str(os.path.join(str(BASE_DIR), '.env')))
    main()
