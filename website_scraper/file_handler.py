import os
from pathlib import Path

from termcolor import colored


class FileHandler:
    def __init__(self):
        self.output_dir = Path(Path.cwd(), "output")
        self._create_path(Path(self.output_dir))

    def _create_path(self, path) -> None:
        """ Creates all directories in the path """
        if not Path.exists(path):
            os.makedirs(path)

    def save_content_to_file(self, path, filename, content) -> None:
        """ Save the content into a file in the given path. """
        full_path = Path(self.output_dir, path)
        self._create_path(full_path)
        file_path = Path(full_path, filename)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)

    def show_structure(self, dir, count=0):
        """ Show structure of a directory. """
        weight_indent = "".join(["—— " for i in range(count)])
        folders = []
        for element in list(dir.iterdir()):
            if os.path.isfile(element):
                # show file names first
                print(
                    "|{indent}{element}".format(
                        indent=weight_indent, element=element.name
                    )
                )
            else:
                folders.append(element)
        for folder in sorted(folders):
            print(
                "|{indent}{element}".format(
                    indent=weight_indent, element=colored(folder.name, "blue")
                )
            )
            self.show_structure(folder, count + 1)
