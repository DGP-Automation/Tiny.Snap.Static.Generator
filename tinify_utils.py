import tinify


def process_img(local_img_path: str, output_folder: str, api_key: str) -> bool:
    tinify.key = api_key
    if "/" in local_img_path:
        file_name_no_extension = local_img_path.split("/")[-1].split(".")[0]
    elif "\\" in local_img_path:
        file_name_no_extension = local_img_path.split("\\")[-1].split(".")[0]
    else:
        raise ValueError("Invalid file path")
    source = tinify.from_file(local_img_path)
    converted = source.convert(type="image/png")
    extension = converted.result().extension
    output_file_path = output_folder + "/" + file_name_no_extension + "." + extension
    converted.to_file(output_file_path)
    return True
