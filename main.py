import logging
from pathlib import Path

from PIL import Image

PARENT_DIR = Path().resolve()
INPUT_FOLDER_NAME = 'input'
OUTPUT_FOLDER_NAME = 'output'
INPUT_DIR = PARENT_DIR / INPUT_FOLDER_NAME
OUTPUT_DIR = PARENT_DIR / OUTPUT_FOLDER_NAME
INCOMING_IMAGES = INPUT_DIR.rglob('**/*')
QUALITY_PERCENT = 95
WIDTH_TO_HEIGHT_PERCENT_3_4 = 33.33     # 3:4 ratio


def crop_center(pil_img: Image, crop_width: int, crop_height: int) -> Image:
    """
    A function for cropping the image in the center.

    :param pil_img: A PIL Image object with the source file.
    :param crop_width: The width of the new image.
    :param crop_height: Height of the new image.
    :return: A new instance of the PIL Image with a cropped image.
    """
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))


def get_save_path(photo_path: Path) -> Path:
    """
    Returns the path to save the cropped image.

    :param photo_path: Path to the source image file.
    :return: The path to save the modified image file.
    """
    save_dir_path = Path(str(photo_path.parent).replace(f'/{INPUT_FOLDER_NAME}/', f'/{OUTPUT_FOLDER_NAME}/'))
    if save_dir_path == INPUT_DIR:
        save_dir_path = OUTPUT_DIR
    prepare_dir(save_dir_path)
    return save_dir_path / photo_path.name


def prepare_dir(save_dir_path: Path) -> None:
    """
    Creates a folder to save the edited image.

    :param save_dir_path: The path to save the new image file.
    """
    if not save_dir_path.is_dir():
        save_dir_path.mkdir(parents=True)


def get_new_height(width: int) -> int:
    """
    Adds a specified percentage to the width of the original image. 
    For the 3:4 format, the width is increased by 33%.

    :param width: The width of the original image.
    :return: Height of the new image.
    """
    difference = WIDTH_TO_HEIGHT_PERCENT_3_4 * (float(width) / 100)
    new_height = round(width + difference)
    return new_height


def main():
    """
    Processes incoming images. Saves cropped images.
    """
    file_counter = 0
    all_paths = list(INCOMING_IMAGES)
    photos = set([photo_path for photo_path in all_paths if photo_path.is_file()])
    for photo in photos:
        save_file_path = get_save_path(photo_path=photo)

        with Image.open(photo) as image:
            width, height = image.size
            if width > height:
                logging.warning(f'{photo.name} - width is higher then height. File skipped.')
                continue
            new_height = get_new_height(width)
            im_crop = crop_center(pil_img=image, crop_width=width, crop_height=new_height)

        im_crop.save(save_file_path, quality=QUALITY_PERCENT)
        logging.info(f'File saved: {save_file_path}')
        file_counter += 1

    logging.info(f'All files processed. Input {len(photos)}, Output {file_counter}, All paths {len(all_paths)}')


if __name__ == '__main__':
    logging.basicConfig(level='INFO')
    main()
