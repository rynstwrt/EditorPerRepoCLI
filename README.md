# EditorPerRepo
 Open a different editor per repo when opening a repo on GitHub Desktop!

<br>

## FEATURES:
- Config to set what file types go to what editor.
- Config allows for setting a default editor.
- Ability to force a repository to use any editor by creating a `.editor-config` file in the root of the repository with a single line containing the path to the editor's executable.
- Support for **glob patterns** and **environment variables** in paths.

<br>

## SETUP:
1. In GitHub Desktop: File > Options > Integrations > Configure custom editor...
2. Set the path to a **pythonw** executable.
   - Running with `pythonw.exe` instead of `python.exe` prevents showing a console window.
3. Set the arguments to the path to the downloaded repo's `main.pyw` file with a space and `%TARGET_PATH%` after it.
   - Ex: `%HOME%\Documents\GitHub\EditorPerRepo\main.pyw %TARGET_PATH%`
4. Set up your favorite editors in the `config.toml` file.
5. That's it!

<br>

## CONFIG:
```toml
#-----------------------------------------------------------------------------------------
# Set which editors to use based on the kinds of files present in each repository.
# Environment variables such as %LocalAppData% are supported.
# Glob patterns are also supported.

# You can also force a repo to use a given editor by creating a file named ".repo-editor"
# in the root of the repo with one line containing the editor's path.
#-----------------------------------------------------------------------------------------


# Editors to use for repos containing these file types.
# If multiple of these file types are present, it will use the most prevalent one.
[[editors]]
extensions = [".py", ".pyw"]
editor = "C:/Program Files/JetBrains/*/*/pycharm64.exe"

[[editors]]
extensions = [".js", ".css", ".html"]
editor = "C:/Program Files/JetBrains/*/*/webstorm64.exe"

[[editors]]
default = true
editor = "%LocalAppData%/Programs/Microsoft VS Code/Code.exe"


# NOTE: You can also format the config like this!
#editors = [
#    { extensions = [".py", ".pyw"], editor = "C:/Program Files/JetBrains/*/*/pycharm64.exe" },
#    { extensions = [".js", ".css", ".html"], editor = "C:/Program Files/JetBrains/*/*/webstorm64.exe" },
#    { default = true, editor = "%LocalAppData%/Programs/Microsoft VS Code/Code.cmd" },
#]
```