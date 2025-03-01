from pathlib import Path
import sys
import subprocess
import json


EDITOR_FILE_TYPE_CONFIG = "./editor-file-types.json"


def attempt_file_read(file_path):
    try:
        return open(file_path, "r")
    except OSError as err:
        return err


def detect_editor_from_file_types(repo_dir):
    file_content = attempt_file_read(repo_dir.joinpath(EDITOR_FILE_TYPE_CONFIG))

    if isinstance(file_content, Exception):
        print("Error: Editor config file could not be read!")
        return print(file_content)

    data = json.load(file_content)

    extensions = data.keys()
    most_common_file_type = None
    for extension in extensions:
        files_of_type = repo_dir.glob(f"*{extension}")
        num_files = len(list(files_of_type))
        if num_files and (not most_common_file_type or most_common_file_type[1] < num_files):
            most_common_file_type = (extension, num_files)

    if not most_common_file_type:
        return print("Error: No file types with an associated editor were found!")

    file_type, num_files = most_common_file_type
    print(f"Most common file extension is {file_type} with {num_files} files found.")

    editor_info = data[file_type]
    print(editor_info)

    parent_dir = editor_info["parentDir"]
    exec_name = editor_info["executableName"]
    print(parent_dir, exec_name)

    parent_dir_path = Path(parent_dir)
    exec_path = list(parent_dir_path.glob(f"**/{exec_name}"))
    print(f"Found executable path at {exec_path}!")

    return exec_path


def main(repo_dir):
    repo_dir = Path(repo_dir)
    print(f"Repo dir: {repo_dir}")

    if not repo_dir.exists():
        print("Error: Given repo directory does not exist!")
        return

    detected_editor = detect_editor_from_file_types(repo_dir)
    if not detected_editor:
        return

    subprocess.call([detected_editor[0], repo_dir])


if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args):
        main(args[0])
    else:
        print("Error: No path to open was passed to this script!")