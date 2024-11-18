import threading
import tinify
import os

from tinify import AccountError

from config.config import TINY_PNG_API_LIST

ALLOWED_MIME = [
    "jpg",
    "png",
    "webp"
]

lock = threading.Lock()
api_index = 0


def process_img(local_img_path: str, output_folder: str, convert_to: str = None) -> bool:
    # Check for allowed MIME type
    if convert_to not in ALLOWED_MIME and convert_to is not None:
        print(f"{convert_to} is not an allowed MIME type")
        return False

    # Extract file name and extension safely
    file_name = os.path.basename(local_img_path)
    origin_type = os.path.splitext(file_name)[-1].lstrip(".")

    if not origin_type:
        raise ValueError("Unable to determine the file type")

    # Create full output path with updated extension
    converted_extension = convert_to if convert_to else origin_type
    output_file_name = file_name.replace(origin_type, converted_extension)
    output_file_path = os.path.join(output_folder, output_file_name)

    # Process image with Tinify
    tinify.key = TINY_PNG_API_LIST[api_index]
    source = tinify.from_file(local_img_path)
    if convert_to and origin_type != convert_to:
        source = source.convert(type=f"image/{convert_to}")
    source.to_file(output_file_path)
    print(f"Compressed {local_img_path} to {output_file_path} with API key {tinify.key}")
    return True


def change_api_key(e):
    if lock.locked():
        return
    with lock:
        global api_index
        print(f"API key {tinify.key} has reached its limit -> {str(e)}")
        api_index += 1
        if api_index >= len(TINY_PNG_API_LIST):
            raise RuntimeError("All API keys have reached their limit")
        tinify.key = TINY_PNG_API_LIST[api_index]
        print(f"API Key changed to {TINY_PNG_API_LIST[api_index]} at index {api_index}")
