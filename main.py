from pathlib import Path
import sys
import subprocess


def main(repo_dir):
    repo_dir = Path(repo_dir)
    print(f"Repo dir: {repo_dir}")

    if not repo_dir.exists():
        print("Error: Given repo directory does not exist!")
        return

    editor_config_file = repo_dir.joinpath(".repo-editor")
    if not editor_config_file.exists():
        return print("Error: .repo-editor file was not found in that repo!")

    editor_command = open(editor_config_file, "r").read()
    print("command:", editor_command)

    # subprocess.call([editor_command, repo_dir])


def parse_args():
    args = sys.argv[1:]
    args.append("Documents/GitHub/EditorPerRepo")
    print(args)

    if not len(args):
        return print("Error: No path to open was passed to this script!")


if __name__ == "__main__":
    my_repo_path = Path.home().joinpath(Path("Documents/GitHub/EditorPerRepo"))
    main(my_repo_path)
