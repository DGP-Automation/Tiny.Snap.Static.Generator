import tinify

ALLOWED_MIME = [
    "jpg",
    "png",
    "webp"
]


def process_img(local_img_path: str, output_folder: str, api_key: str, convert_to: str = None) -> bool:
    if convert_to not in ALLOWED_MIME and convert_to is not None:
        print(f"{convert_to} is not an allowed mime type")
        return False
    origin_type = local_img_path.split(".")[-1]

    tinify.key = api_key
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
    output_file_path = output_folder + "/" + file_name.replace(origin_type, convert_to)
    source.to_file(output_file_path)
    print(f"Compressed {local_img_path} to {output_file_path} with API key {api_key}")
    return True
