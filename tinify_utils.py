import threading

import tinify
from config.config import TINY_PNG_API_LIST

ALLOWED_MIME = [
    "jpg",
    "png",
    "webp"
]

lock = threading.Lock()
api_index = 0


def process_img(local_img_path: str, output_folder: str, convert_to: str = None) -> bool:
    if convert_to not in ALLOWED_MIME and convert_to is not None:
        print(f"{convert_to} is not an allowed mime type")
        return False
    origin_type = local_img_path.split(".")[-1]

    if "/" in local_img_path:
        file_name = local_img_path.split("/")[-1]
    elif "\\" in local_img_path:
        file_name = local_img_path.split("\\")[-1]
    else:
        raise ValueError("Invalid file path")
    source = tinify.from_file(local_img_path)
    if convert_to:
        if origin_type not in convert_to:
            source = source.convert(type=f"image/{convert_to}")
    output_file_path = output_folder + "/" + file_name.replace(origin_type, convert_to if convert_to else origin_type)
    source.to_file(output_file_path)
    print(f"Compressed {local_img_path} to {output_file_path} with API key {tinify.key}")
    return True


def change_api_key(e):
    if lock.locked():
        return
    with lock:
        global api_index
        print(f"API key {tinify.key} has reached its limit -> {e}")
        if api_index >= len(TINY_PNG_API_LIST):
            raise RuntimeError("All API keys have reached their limit")
        api_index += 1
        tinify.key = api_key = TINY_PNG_API_LIST[api_index]
        print(f"API Key changed to {api_key} at index {api_index}")
