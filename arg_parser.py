import argparse


class ArgParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(prog="EditorPerRepo",
                                              description="Open a different editor per repo when opening a repo on GitHub Desktop!")

        self.parser.add_argument("--config",
                                 type=str,
                                 help="Path to a config that's not the default.")

        self.parser.add_argument("--nolaunch",
                                 action="store_true",
                                 help="Run the script, but don't actually launch the editor.")

        self.parser.add_argument("target_dir",
                                 type=str,
                                 help="The directory (repo) for the editor to open.")


    def parse_args(self, args):
        return self.parser.parse_args(args)