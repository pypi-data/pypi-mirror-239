import time

import openai
from utils_base import Log
from utils_www import WWW

log = Log('AIDraw')


class AIImage:
    DEFAULT_N_IMAGES = 1
    DEFAULT_SIZE = '1024x1024'

    def draw(
        self, description: str, image_path: str, size: str = None
    ) -> str:
        size = size or AIImage.DEFAULT_SIZE

        tic = time.perf_counter()
        response = openai.Image.create(
            prompt=description, n=AIImage.DEFAULT_N_IMAGES, size=size
        )
        image_url = response['data'][0]['url']
        log.debug(f'Generated "{description}" -> {image_url}')
        WWW.download_binary(image_url, image_path)
        toc = time.perf_counter()
        log.info(
            f'Downloaded "{image_url}" -> {image_path} ({toc - tic:0.4f}s)'
        )
