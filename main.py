import os
import tinify
import concurrent.futures
import multiprocessing
from tinify_utils import process_img, change_api_key
from tkinter import Tk
from tkinter.filedialog import askdirectory

convert_type_to = None  # "webp"


def list_resources(snap_static_base_path: str, tiny_snap_static_base_path: str) -> list:
    # list all png files in the snap_static_base_path including subdirectories
    png_resource_list = []
    for root, dirs, files in os.walk(snap_static_base_path):
        for file in files:
            if file.endswith(".png") or file.endswith(".jpg"):
                png_resource_list.append({
                    "snap_static_file": os.path.join(root, file).replace("\\", "/"),
                    "tiny_snap_static_file": os.path.join(root, file).replace(snap_static_base_path,
                                                                              tiny_snap_static_base_path).replace("\\",
                                                                                                                  "/"),
                    "tiny_snap_static_path": root.replace(snap_static_base_path,
                                                          tiny_snap_static_base_path).replace("\\", "/")
                })
    tiny_task_list = []
    # Check if the file exists in the tiny_snap_static_base_path
    for png_task in png_resource_list:
        tiny_snap_static_file = png_task["tiny_snap_static_file"]
        if not os.path.exists(tiny_snap_static_file):
            tiny_task_list.append(png_task)
            if not os.path.exists(png_task["tiny_snap_static_path"]):
                print(f"Creating directory {png_task['tiny_snap_static_path']}")
                os.makedirs(png_task["tiny_snap_static_path"])
    return tiny_task_list


def main():
    device_runtime = os.getenv("device_runtime")
    if device_runtime == "masterain":
        png_task_list = list_resources(r"C:\Users\i\Documents\GitHub\Snap.Static",
                                       r"C:\Users\i\Documents\GitHub\Snap.Static.Tiny")
    elif device_runtime == "actions":
        png_task_list = list_resources(r"./Snap.Static",
                                       r"./Snap.Static.Tiny")
    else:
        root = Tk()
        root.withdraw()
        snap_static_base_path = askdirectory(title="Select the Folder of Snap.Static")
        tiny_snap_static_base_path = askdirectory(title="Select the Folder of Snap.Static.Tiny")
        if any(not x for x in [snap_static_base_path, tiny_snap_static_base_path]):
            raise ValueError("Invalid folder path")
        png_task_list = list_resources(snap_static_base_path, tiny_snap_static_base_path)
    print(f"Total number of tasks: {len(png_task_list)}")

    def process_png_task(png_task):
        while True:
            try:
                process_img(png_task["snap_static_file"], png_task["tiny_snap_static_path"], convert_type_to)
                break
            except tinify.AccountError as e:
                change_api_key(e)

    num_cores = multiprocessing.cpu_count()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_cores) as executor:
        futures = [executor.submit(process_png_task, png_task) for png_task in png_task_list]
        for future in concurrent.futures.as_completed(futures):
            print(f"Task completed: {future.result()}")


if __name__ == "__main__":
    main()
