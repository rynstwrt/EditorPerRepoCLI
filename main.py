from pathlib import Path
import sys
import subprocess
import tomllib
import glob


EDITOR_FILE_TYPE_CONFIG = "config.toml"


def load_config(config_path):
    try:
        config_content = open(config_path, "rb")
        return tomllib.load(config_content)
    except (OSError, tomllib.TOMLDecodeError) as err:
        return err


def detect_editor_from_file_types(repo_dir):
    config_data = load_config(repo_dir.joinpath(EDITOR_FILE_TYPE_CONFIG))
    print(config_data)

    if isinstance(config_data, Exception):
        print("Error: Config file could not be loaded!")
        return print(config_data)

    config_tables = config_data.keys()
    editor_table = config_data["editors"] if "editors" in config_tables else None
    miscellaneous_table = config_data["miscellaneous"] if "miscellaneous" in config_tables else None
    print(editor_table)
    print(miscellaneous_table)

    default_editor = miscellaneous_table["default_editor"] if miscellaneous_table and "default_editor" in miscellaneous_table else None
    print(default_editor)

    if not editor_table and not default_editor:
        return print("Error: No editor assignments made and no default editor is set!")

    extensions = editor_table.keys()
    most_common_file_type = None
    for extension in extensions:
        files_of_type = repo_dir.glob(f"*{extension}")
        num_files = len(list(files_of_type))
        if num_files and (not most_common_file_type or most_common_file_type[1] < num_files):
            most_common_file_type = (extension, num_files)

    if not most_common_file_type:
        return default_editor
        # return print("Error: No file types with an associated editor were found!")

    file_type, num_files = most_common_file_type
    print(f"Most common file extension is {file_type} with {num_files} files found.")

    return editor_table[file_type]


def main(repo_dir):
    repo_dir = Path(repo_dir)

    if not repo_dir.exists():
        print("Error: Given repo directory does not exist!")
        return

    given_editor_location = detect_editor_from_file_types(repo_dir)
    if not given_editor_location:
        return print("Error: No valid editor locations could be found!")

    editor_path_search_results = glob.glob(given_editor_location, recursive=True)
    editor_path = editor_path_search_results[0] if editor_path_search_results else None

    if not editor_path:
        return print(f'Error: Editor at "{given_editor_location}" could not be found!')
        # return print(f'Error: Assigned editor for {file_type} files "{config_editor_location}" could not be found!')

    print(f"Found executable path at {editor_path}!")
    subprocess.call([editor_path, repo_dir])


if __name__ == "__main__":
    args = sys.argv[1:]

    if len(args):
        main(args[0])
    else:
        print("Error: No path to open was passed to this script!")