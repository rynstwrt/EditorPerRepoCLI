from pathlib import Path
from os.path import expandvars
import sys
import subprocess
import glob
from config_manager import ConfigManager


CONFIG_LOCATION = "config.toml"


def detect_editor_from_file_types(repo_dir, editor_table):
    file_extensions = editor_table.keys()

    most_common_file_type = None
    for extension in file_extensions:
        files_of_type = repo_dir.glob(f"*{extension}")
        num_files = len(list(files_of_type))
        if num_files and (not most_common_file_type or most_common_file_type[1] < num_files):
            most_common_file_type = (extension, num_files)

    if not most_common_file_type:
        return

    file_type, num_files = most_common_file_type
    print(f"Most common file extension is {file_type} with {num_files} files found.")

    return editor_table[file_type]


def get_repo_editor(repo_dir):
    config_load_result = config_manager.load_config(repo_dir.joinpath(CONFIG_LOCATION))

    if isinstance(config_load_result, Exception):
        print("Error: Config file could not be loaded!")
        return print(config_load_result)

    editor_table = config_manager.get_editor_table()
    default_editor = config_manager.get_default_editor()
    if not editor_table:
        return default_editor if default_editor else print("Error: No editor assignments made and no default editor is set!")

    detected_editor = detect_editor_from_file_types(repo_dir, editor_table)
    if not detected_editor:
        return default_editor

    return detected_editor


def main(repo_dir):
    repo_dir = Path(repo_dir)

    if not repo_dir.exists():
        print("Error: Given repo directory does not exist!")
        return

    given_editor_location = get_repo_editor(repo_dir)
    if not given_editor_location:
        return print("Error: No valid editor locations could be found!")

    given_editor_location = expandvars(given_editor_location)

    editor_path_search_results = glob.glob(given_editor_location, recursive=True)
    editor_path = editor_path_search_results[0] if editor_path_search_results else None

    if not editor_path:
        return print(f'Error: Editor at "{given_editor_location}" could not be found!')

    print(f"Found executable path at {editor_path}!")
    # subprocess.call([editor_path, repo_dir])


if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args):
        config_manager = ConfigManager()
        main(args[0])
    else:
        print("Error: No path to open was passed to this script!")