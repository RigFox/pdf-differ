from typing import Literal
from pdf2image import convert_from_path
from pathlib import Path
from PIL import Image, ImageChops
from os import cpu_count

PDFS = Path(__file__).parent / 'pdfs'
RESULT = Path(__file__).parent / 'result'
RESULT_DIFF = RESULT / 'diff'


def convert(filepath: str, output_dir: any):
    def filename_generator():
        i = 0

        while True:
            i += 1
            yield str(i)

    convert_from_path(filepath, fmt='jpg', output_file=filename_generator(),
                      output_folder=output_dir, thread_count=cpu_count())


def find_page(i: int, folder: str):

    prefix = '0' if i < 10 else ''
    image = list(Path(folder).glob(f'?-{prefix}{i}.jpg'))

    if len(image) != 1:
        raise ValueError(f'Can\'t find page {i}')

    return image[0]


def diff(page: int, path1: Path, path2: Path, output_dir):
    img1 = Image.open(path1)
    img2 = Image.open(path2)

    diff = ImageChops.difference(img1, img2)

    # Images have same size
    dst = Image.new('RGB', (img1.width + img2.width + diff.width, img1.height))
    dst.paste(img1, (0, 0))
    dst.paste(img2, (img1.width, 0))
    dst.paste(diff, (img1.width + img2.width, 0))
    dst.save(f'{output_dir}/{page}.jpg')


def diff_all(old_dir, new_dir, output_dir):
    old_count = len(list(Path(old_dir).glob('*.jpg')))
    new_count = len(list(Path(new_dir).glob('*.jpg')))
    diff_count = min(old_count, new_count)

    if (old_count != new_count):
        print('Warning: Count of pages is not the same')
        print(f'Old pages: {old_count}')
        print(f'New pages: {new_count}')

    print(f'Diff {diff_count} pages')

    for i in range(1, diff_count + 1):
        old_image = find_page(i, old_dir)
        new_image = find_page(i, new_dir)

        diff(i, old_image, new_image, output_dir)
