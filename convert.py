from typing import Literal
from pdf2image import convert_from_path
from pathlib import Path
from PIL import Image, ImageChops
from os import cpu_count

PDFS = Path(__file__).parent / 'pdfs'
RESULT = Path(__file__).parent / 'result'
RESULT_OLD = RESULT / 'old'
RESULT_NEW = RESULT / 'new'
RESULT_DIFF = RESULT / 'diff'


def get_folder(filename: Literal['old', 'new']):
    return RESULT_OLD if filename == 'old' else RESULT_NEW

def create_folders():
    RESULT_OLD.mkdir(parents=True, exist_ok=True)
    RESULT_NEW.mkdir(parents=True, exist_ok=True)
    RESULT_DIFF.mkdir(parents=True, exist_ok=True)

def cleanup(path: Path):
    for file in path.iterdir():
        if not file.is_dir():
            file.unlink()


def cleanup_all():
    cleanup(RESULT_OLD)
    cleanup(RESULT_NEW)
    cleanup(RESULT_DIFF)


def convert(filepath: str, output_dir: any):
    def filename_generator():
        i = 0

        while True:
            i += 1
            yield str(i)

    convert_from_path(filepath, fmt='jpg', output_file=filename_generator(),
                      output_folder=output_dir, thread_count=cpu_count())


def convert_pdfs():
    convert('old')
    convert('new')


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


if __name__ == '__main__':
    create_folders()
    cleanup_all()
    convert_pdfs()
    diff_all()
