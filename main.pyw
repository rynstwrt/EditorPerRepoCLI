from functools import reduce
from pathlib import Path
from os.path import expandvars
from config_manager import ConfigManager
from importlib.util import find_spec
import sys
import subprocess
import glob


CONFIG_PATH = "./config.toml"
FORCED_EDITOR_FILE_NAME = ".repo-editor"


def detect_editor_from_file_types(repo_dir, editor_entries):
    most_common_file_type = None
    for entry in editor_entries:
        if "default" in entry and "extensions" not in entry:
            continue

        extensions, editor_path = entry["extensions"], entry["editor"]

        extension_search_results = [list(repo_dir.glob(f"*{extension}")) for extension in extensions]

        files_of_types = reduce(lambda a, b: a + b, extension_search_results)
        if files_of_types:
            num_files_of_types = len(files_of_types)
            if not most_common_file_type or num_files_of_types > most_common_file_type[0]:
                most_common_file_type = (num_files_of_types, entry)

    if most_common_file_type:
        return most_common_file_type[1]["editor"]


def get_repo_editor(repo_dir):
    forced_editor = config_manager.get_forced_editor_from_file(repo_dir, FORCED_EDITOR_FILE_NAME)
    if forced_editor:
        print(f'Found {FORCED_EDITOR_FILE_NAME} file with path to "{forced_editor}"!')
        return forced_editor

    # TODO:
    config_load_result = config_manager.load_config(repo_dir.joinpath(CONFIG_PATH))
    if isinstance(config_load_result, Exception):
        print("[ERROR] Config file could not be loaded!")
        return print(config_load_result)

    editor_entries = config_manager.get_editor_entries()
    default_editor = config_manager.get_default_editor()
    if not editor_entries:
        return default_editor if default_editor else print("[ERROR] No editor assignments made and no default editor is set!")

    return detect_editor_from_file_types(repo_dir, editor_entries) or default_editor


def main(repo_dir):
    repo_dir = Path(repo_dir)

    if not repo_dir.exists():
        print("[ERROR] Given repo directory does not exist!")
        return

    given_editor_location = get_repo_editor(repo_dir)
    if not given_editor_location:
        return print("[ERROR] No valid editor locations could be found!")

    given_editor_location = expandvars(given_editor_location)

    editor_path_search_results = glob.glob(given_editor_location, recursive=True)
    editor_path = editor_path_search_results[0] if editor_path_search_results else None

    if not editor_path:
        return print(f'[ERROR] Editor at "{given_editor_location}" could not be found!')

    print(f"Found executable path at {editor_path}!")

    if not dev_util or dev_util.RUN_EDITOR_WHEN_FOUND:
        subprocess.Popen([editor_path, repo_dir])


if __name__ == "__main__":
    dev_util = None
    if find_spec("util.dev_util"):
        from util.dev_util import DevUtil
        print("Loaded dev_util")
        dev_util = DevUtil()
        CONFIG_PATH = dev_util.CONFIG_PATH

    args = sys.argv[1:]

    if len(args):
        config_manager = ConfigManager()
        main(args[0])
    else:
        print("[ERROR] No path to open was passed to this script!")