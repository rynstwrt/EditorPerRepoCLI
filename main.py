from pathlib import Path
import sys
import subprocess
import yaml


CONFIG_FILE_NAME = ".repo-editor"

CONFIG_EDITOR_KEY = "editor_path"
CONFIG_EDITOR_ARGS_KEY = "editor_args"
REQUIRED_CONFIG_KEYS = [CONFIG_EDITOR_KEY]


def read_config(config_path):
    with open(config_path) as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            return None


def main(repo_dir):
    repo_dir = Path(repo_dir)
    print(f"Repo dir: {repo_dir}")

    if not repo_dir.exists():
        print("Error: Given repo directory does not exist!")
        return

    editor_config_file = repo_dir.joinpath(CONFIG_FILE_NAME)
    print(editor_config_file)
    if not editor_config_file.exists():
        return print(f"Error: {CONFIG_FILE_NAME} file was not found in that repo!")

    config_data = read_config(editor_config_file)
    if not config_data:
        return print("Error: Config data could not be read!")

    config_keys = config_data.keys()

    missing_config_keys = []
    for key in REQUIRED_CONFIG_KEYS:
        if key not in config_keys:
            missing_config_keys.append(key)

    if missing_config_keys:
        return print(f"Error: Required config keys {missing_config_keys} were not found!")

    editor_path = config_data[CONFIG_EDITOR_KEY]
    editor_args = [] if CONFIG_EDITOR_ARGS_KEY not in config_keys else config_data[CONFIG_EDITOR_ARGS_KEY]
    print(editor_path, editor_args)

    subprocess.call([editor_path, *editor_args, repo_dir])


if __name__ == "__main__":
    args = sys.argv[1:]
    print("args: ", args)

    if not len(args):
        print("Error: No path to open was passed to this script!")
    else:
        main(args[0])
        # main(Path.home().joinpath(Path("Documents/GitHub/EditorPerRepo")))