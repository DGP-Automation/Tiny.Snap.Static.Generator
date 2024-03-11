import os
import tinify
import concurrent.futures
import multiprocessing
import threading
from config.config import TINY_PNG_API_LIST
from tinify_utils import process_img
from tkinter import Tk
from tkinter.filedialog import askdirectory

api_index = 0


def list_resources(snap_static_base_path: str, tiny_snap_static_base_path: str) -> list:
    # list all png files in the snap_static_base_path including subdirectories
    png_resource_list = []
    for root, dirs, files in os.walk(snap_static_base_path):
        for file in files:
            if file.endswith(".png"):
                png_resource_list.append({
                    "snap_static_file": os.path.join(root, file),
                    "tiny_snap_static_file": os.path.join(root, file).replace(snap_static_base_path,
                                                                              tiny_snap_static_base_path),
                    "tiny_snap_static_path": root.replace(snap_static_base_path, tiny_snap_static_base_path)
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
        png_task_list = list_resources(snap_static_base_path, tiny_snap_static_base_path)
    print(f"Total number of tasks: {len(png_task_list)}")
    api_index_lock = threading.Lock()

    def process_png_task(png_task):
        global api_index
        while True:
            api_key = TINY_PNG_API_LIST[api_index]
            try:
                process_result = process_img(png_task["snap_static_file"], png_task["tiny_snap_static_path"], api_key)
                if process_result:
                    print(f"Successfully process file {png_task['snap_static_file']} with KEY {api_index}")
                break
            except tinify.AccountError as e:
                print(f"API key {api_key} has reached its limit -> {e}")

                with api_index_lock:
                    if api_index >= len(TINY_PNG_API_LIST):
                        raise RuntimeError("All API keys have reached their limit")
                    api_index += 1
                    api_key = TINY_PNG_API_LIST[api_index]
                    print(f"API Key changed to {api_key} at index {api_index}")

    num_cores = multiprocessing.cpu_count()
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_cores) as executor:
        futures = [executor.submit(process_png_task, png_task) for png_task in png_task_list]
        for future in concurrent.futures.as_completed(futures):
            pass


if __name__ == "__main__":
    main()
