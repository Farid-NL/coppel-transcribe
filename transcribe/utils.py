import os


def convert_files_to_utf8(directory_path: str) -> bool:
    """
    Convert UTF-16 encoded files to UTF-8 encoded files.
    :param directory_path: Directory where UTF-16 encoded files are located.
    :return: `True` if all files were UTF-8 encoded successfully, `False` otherwise.
    """

    def utf16_to_utf8(file_path: str):
        with open(file_path, "rb") as source:
            data = source.read().decode("utf-16").encode("utf-8")

        with open(file_path, "wb") as dest:
            dest.write(data)

    full_path = os.path.abspath(directory_path)
    files = os.listdir(full_path)

    for file in files:
        try:
            utf16_to_utf8(os.path.join(full_path, file))
        except UnicodeDecodeError:
            return False

    return True
