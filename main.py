from pathlib import Path
import sys
import subprocess
import yaml


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

    editor_config_file = repo_dir.joinpath("repo-editor.yaml")
    print(editor_config_file)
    if not editor_config_file.exists():
        return print("Error: repo-editor.yaml file was not found in that repo!")

    config_data = read_config(editor_config_file)
    if not config_data:
        return print("Error: Config data could not be read!")

    editor_path = config_data["editor_path"]
    editor_args = config_data["editor_args"]
    print(editor_path, editor_args)

    subprocess.call([editor_path, *editor_args, repo_dir])


def parse_args():
    args = sys.argv[1:]
    args.append("Documents/GitHub/EditorPerRepo")
    print(args)

    if not len(args):
        return print("Error: No path to open was passed to this script!")


if __name__ == "__main__":
    my_repo_path = Path.home().joinpath(Path("Documents/GitHub/EditorPerRepo"))
    main(my_repo_path)
