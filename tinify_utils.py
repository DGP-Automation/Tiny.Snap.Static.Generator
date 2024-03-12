import tinify


def process_img(local_img_path: str, output_folder: str, api_key: str) -> bool:
    tinify.key = api_key
    if "/" in local_img_path:
        file_name = local_img_path.split("/")[-1]
    elif "\\" in local_img_path:
        file_name = local_img_path.split("\\")[-1]
    else:
        raise ValueError("Invalid file path")
    source = tinify.from_file(local_img_path)
    #converted = source.convert(type="image/png")
    #extension = converted.result().extension
    output_file_path = output_folder + "/" + file_name
    source.to_file(output_file_path)
    print(f"Compressed {local_img_path} to {output_file_path} with API key {api_key}")
    return True
