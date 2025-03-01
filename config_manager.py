import tomllib


class ConfigManager:
    def __init__(self):
        self.editor_table = None
        self.default_editor = None


    def load_config(self, config_path):
        try:
            config_content = open(config_path, "rb")
            config_data = tomllib.load(config_content)

            config_tables = config_data.keys()

            self.editor_table = config_data["editors"] if "editors" in config_tables else None

            miscellaneous_table = config_data["miscellaneous"] if "miscellaneous" in config_tables else None
            self.default_editor = miscellaneous_table["default_editor"] if miscellaneous_table and "default_editor" in miscellaneous_table else None
        except (OSError, tomllib.TOMLDecodeError) as err:
            return err


    def get_editor_table(self):
        return self.editor_table


    def get_default_editor(self):
        return self.default_editor