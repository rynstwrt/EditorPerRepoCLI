from pathlib import Path
import sys
import subprocess
import yaml


CONFIG_FILE_NAME = ".repo-editor"


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

    if "editor_path" not in config_keys:
        return print(f"Error: editor_path was not set in {CONFIG_FILE_NAME}!")

    editor_path = config_data["editor_path"]

    editor_args = [] if "editor_args" not in config_keys else config_data["editor_args"]
    print(editor_path, editor_args)

    subprocess.call([editor_path, *editor_args, repo_dir])


def parse_args():
    args = sys.argv[1:]
    print("args: ", args)

    if not len(args):
        return print("Error: No path to open was passed to this script!")

    main(args[0])
    # main(Path.home().joinpath(Path("Documents/GitHub/EditorPerRepo")))


if __name__ == "__main__":
    parse_args()
