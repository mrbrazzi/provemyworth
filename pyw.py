"""
How to Prove My Worth

My name is Alain Sánchez Gutiérrez (https://about.me/mr.brazzi).

I'm a Software Developer and Father, both at full time. I like self-learn and I learn quick. I enjoy teach what I learn. I believe in teamwork and help teammates when they need.

This exam was developed on Windows 10 with Python 3.6 using PyCharm 2020.1.
"""
from pathlib import Path

import requests
from PIL import Image, ImageDraw
from bs4 import BeautifulSoup


class ProveMyWorth:
    the_name = 'Alain Sanchez Gutierrez'
    the_email = 'brazzisoft.com@gmail.com'
    the_username = 'mr.brazzi'
    the_cv = 'cv_alain_sanchez_gutierrez.pdf'
    the_code = 'pyw.py'
    the_about_me = "I am a Software Developer and Father, both at full time. " \
                   "I like self-learn and I learn quick. I enjoy teach what I learn. " \
                   "I believe in teamwork and help teammates when they need."
    the_hash = None
    the_signed_filename = 'bmw_for_life.jpg'
    the_user_agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'}
    base_url = 'https://www.proveyourworth.net/level3'
    base_dir = None
    session = None

    def __init__(self):
        self.base_dir = Path('.')
        self.session = requests.Session()

    def sign_payload(self, input_image: bytes, output_image_name: str, text: str, pos=None) -> None:
        photo = Image.open(input_image)
        drawing = ImageDraw.Draw(photo)
        pos = pos if pos else (photo.width / 8, photo.height / 2)
        drawing.text(pos, text, fill=(255, 69, 0))
        photo.save(self.base_dir / output_image_name, "JPEG")

    @staticmethod
    def check_url(url: str) -> str:
        return url.replace('http', 'https') if 'https' not in url else url

    @staticmethod
    def print_log(txt: str) -> None:
        print(txt)

    def request_start(self) -> None:
        response = self.session.get(url=f'{self.base_url}/start', headers=self.the_user_agent)
        # self.print_log(f'*** Start ***\nSTATUS: {response.status_code}\n')
        soup = BeautifulSoup(response.content, 'html.parser')
        self.the_hash = soup.find('input', {'name': 'statefulhash'})['value']
        # self.print_log(f'HASH: {self.the_hash}\n\n')
        self.request_activate()

    def request_activate(self) -> None:
        response = self.session.get(url=f'{self.base_url}/activate?statefulhash={self.the_hash}&username={self.the_username}',
                                    headers=self.the_user_agent)
        # self.print_log(f'*** Activate ***\nSTATUS: {response.status_code}\nHEADERS: {response.headers}\nPAYLOAD-URL: {response.headers["X-Payload-URL"]}\n\n')
        self.request_payload(url=self.check_url(response.headers['X-Payload-URL']))

    def request_payload(self, url: str) -> None:
        response = self.session.get(url=url, stream=True, headers=self.the_user_agent)
        # self.print_log(f'\n*** Payload ***\nSTATUS: {response.status_code}\nHEADERS: {response.headers}\nPOSTBACK-URL: {response.headers["X-Post-Back-To"]}\n\n')
        self.sign_payload(input_image=response.raw, output_image_name=self.the_signed_filename,
                          text=f'{self.the_name}\nHash: {self.the_hash}')
        self.request_postback(url=self.check_url(response.headers['X-Post-Back-To']))

    def request_postback(self, url: str) -> None:
        with open(self.base_dir / self.the_cv, 'rb') as resume_file, \
                open(self.base_dir / self.the_signed_filename, 'rb') as signed_image_file, \
                open(self.base_dir / self.the_code, 'rb') as code_file:
            post_data = {'email': self.the_email, 'name': self.the_name, 'aboutme': self.the_about_me}
            post_files = {'image': (self.the_signed_filename, signed_image_file),
                          'code': (self.the_code, code_file),
                          'resume': (self.the_cv, resume_file)}
            response = self.session.post(url, data=post_data, files=post_files, headers=self.the_user_agent)
            self.print_log(f'\n*** Post Back ***\nSTATUS: {response.status_code}'
                           # f'\n\n**** REQUEST ****\nHEADER: {response.request.headers}'
                           f'\n\n**** RESPONSE ****\nHEADER: {response.headers}\nBODY:\n{response.text}')


if __name__ == "__main__":
    pmw = ProveMyWorth()
    pmw.request_start()
