import tinify


def process_img(local_img_path: str, output_folder: str, api_key: str, convert_to_png: bool = False) -> bool:
    tinify.key = api_key
    file_type = local_img_path.split(".")[-1]
    if "/" in local_img_path:
        file_name = local_img_path.split("/")[-1]
    elif "\\" in local_img_path:
        file_name = local_img_path.split("\\")[-1]
    else:
        raise ValueError("Invalid file path")
    source = tinify.from_file(local_img_path)
    if convert_to_png and file_type != "png":
        source = source.convert(type="image/png")
    output_file_path = output_folder + "/" + file_name
    source.to_file(output_file_path)
    print(f"Compressed {local_img_path} to {output_file_path} with API key {api_key}")
    return True
