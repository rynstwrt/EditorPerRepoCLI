from pathlib import Path
import sys
import subprocess


CONFIG_FILE_NAME = ".repo-editor"


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

    editor_command = open(editor_config_file).read()
    print(editor_command)
    if not editor_command:
        return print("Error: Config data could not be read!")

    subprocess.call([editor_command, repo_dir])


if __name__ == "__main__":
    args = sys.argv[1:]
    print("args: ", args)

    if not len(args):
        print("Error: No path to open was passed to this script!")
    else:
        main(args[0])
        # main(Path.home().joinpath(Path("Documents/GitHub/EditorPerRepo")))