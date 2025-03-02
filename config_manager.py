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
        invalid_reasons = [has_extensions_or_default, has_editor]
        return {"valid": False not in invalid_reasons, "entry": entry, "reasons": invalid_reasons}


    def __remove_invalid_and_duplicate_entries(self, editor_entries):
        duplicate_entries = []
        for i in range(len(editor_entries) - 1, -1, -1):
            entry = editor_entries[i]
            if entry in editor_entries[:i]:
                duplicate_entries.insert(i, (i, editor_entries.pop(i)))

        if duplicate_entries:
            duplicate_entries.sort()
            print(f"[WARNING] duplicates found in config editor entries!")
            [print(f'\t- Duplicate entry "{entry[1]}" for entry #{entry[0] + 1}') for entry in duplicate_entries]

        invalid_editor_entries = [self.__editor_entry_is_valid(entry) for entry in editor_entries]
        invalid_editor_entries = list(filter(lambda invalid_entry: not invalid_entry["valid"], invalid_editor_entries))

        if invalid_editor_entries:
            print(f"[WARNING] Invalid entries found in config editor entries!")
            for entry_invalid_check_return in invalid_editor_entries:
                entry_needs = [v for i, v in enumerate(["extensions (and/or) default", "editor"]) if not entry_invalid_check_return["reasons"][i]]
                print(f'\t- "{entry_invalid_check_return["entry"]}" -- Missing entry key(s): {entry_needs}')
                editor_entries.remove(entry_invalid_check_return["entry"])


    def load_config(self, config_path: Path):
        try:
            config_content = self.__open_file(config_path, "rb")
            if isinstance(config_content, OSError):
                return config_content

            config_data = tomllib.load(config_content)
            config_file_name = Path(config_path).name

            self.editor_entries = config_data["editors"] if "editors" in config_data else None
            if not self.editor_entries:
                return SyntaxError(f'[ERROR] Section "editors" not found in {config_file_name}!')

            self.__remove_invalid_and_duplicate_entries(self.editor_entries)

            default_editors = [entry for entry in self.editor_entries if "default" in entry and entry["default"] is True]
            if len(default_editors) > 1:
                print("[WARNING] There is more than one default editor defined! The first defined will be used.")
                print("Listed default editors:")
                [print(f'\t{"*" if not i else "-"} {given_default_editor}') for i, given_default_editor in enumerate(default_editors)]

            default_editor = default_editors[0]
            if default_editors and "editor" in default_editor:
                self.default_editor = default_editor["editor"]
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