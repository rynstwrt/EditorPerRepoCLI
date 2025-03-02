from pathlib import Path
import tomllib


class ConfigManager:
    def __init__(self):
        self.editor_entries = None
        self.default_editor = None


    @staticmethod
    def __open_file(file_path, mode="r"):
        try:
            return open(file_path, mode)
        except OSError as err:
            return err


    @staticmethod
    def __editor_entry_is_valid(entry):
        has_extensions_or_default = "extensions" in entry or ("default" in entry and entry["default"] is True)
        has_editor = "editor" in entry
        return has_extensions_or_default and has_editor


    def __remove_invalid_and_duplicate_entries(self, editor_entries):
        duplicate_entries = []
        for i in range(len(editor_entries) - 1, -1, -1):
            entry = editor_entries[i]
            if entry in editor_entries[:i]:
                duplicate_entries.insert(i, (i, editor_entries.pop(i)))

        if duplicate_entries:
            duplicate_entries.sort()
            print(f"Warning: duplicates found in config editor entries!")
            [print(f'\t- Duplicate entry "{entry[1]}" for entry #{entry[0] + 1}') for entry in duplicate_entries]

        invalid_editor_entries = [entry for entry in editor_entries if not self.__editor_entry_is_valid(entry)]
        if invalid_editor_entries:
            print(f"Warning: Invalid entries found in config editor entries!")
            for entry in invalid_editor_entries:
                print(f'\t- {entry} (INVALID)')
                editor_entries.remove(entry)


    def load_config(self, config_path: Path):
        try:
            config_content = self.__open_file(config_path, "rb")
            if isinstance(config_content, OSError):
                return config_content

            config_data = tomllib.load(config_content)
            config_file_name = Path(config_path).name

            self.editor_entries = config_data["editors"] if "editors" in config_data else None
            if not self.editor_entries:
                return SyntaxError(f'Error: Section "editors" not found in {config_file_name}!')

            self.__remove_invalid_and_duplicate_entries(self.editor_entries)

            default_editors = [entry for entry in self.editor_entries if "default" in entry and entry["default"] is True]
            if default_editors and "editor" in default_editors[0]:
                self.default_editor = default_editors[0]["editor"]
                self.editor_entries.remove(default_editors[0])
        except tomllib.TOMLDecodeError as err:
            return err


    def get_forced_editor_from_file(self, repo_dir, forced_editor_file_name):
        forced_editor_file_path = repo_dir / forced_editor_file_name
        if not forced_editor_file_path.exists():
            return

        file_content = self.__open_file(forced_editor_file_path)
        if file_content:
            return file_content.readline()


    def get_editor_entries(self):
        return self.editor_entries


    def get_default_editor(self):
        return self.default_editor