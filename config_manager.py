import tomllib


class ConfigManager:
    def __init__(self):
        self.editor_table = None
        self.default_editor = None


    @staticmethod
    def __open_file(file_path, mode="r"):
        try:
            return open(file_path, mode)
        except OSError as err:
            return err


    def load_config(self, config_path):
        try:
            config_content = self.__open_file(config_path, "rb")
            if isinstance(config_content, OSError):
                return config_content

            config_data = tomllib.load(config_content)

            config_tables = config_data.keys()

            self.editor_table = config_data["editors"] if "editors" in config_tables else None

            miscellaneous_table = config_data["miscellaneous"] if "miscellaneous" in config_tables else None
            self.default_editor = miscellaneous_table["default_editor"] if miscellaneous_table and "default_editor" in miscellaneous_table else None
        except (OSError, tomllib.TOMLDecodeError) as err:
            return err


    def get_forced_editor_from_file(self, repo_dir, forced_editor_file_name):
        forced_editor_file_path = repo_dir / forced_editor_file_name
        if not forced_editor_file_path.exists():
            return

        file_content = self.__open_file(forced_editor_file_path)
        if not file_content:
            return

        return file_content.readline()


    def get_editor_table(self):
        return self.editor_table


    def get_default_editor(self):
        return self.default_editor