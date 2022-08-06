import pathlib
import uuid

from contextlib import contextmanager
from typing import List


@contextmanager
def create_files_with_content(file_name_with_content, folder_path=None) -> List[str]:
    if not folder_path:
        folder_path = f"./tmp-tests-{uuid.uuid4()}"
    folder_absolute_path = _create_dir_if_not_exist_returning_abs_path(folder_path)
    created_files = []

    try:
        for file_name, content in file_name_with_content:
            file_path = pathlib.Path(f"{folder_absolute_path}/{file_name}")

            with open(file_path, mode="a") as file:
                file.writelines(content)

            created_files.append(file_path)

        yield created_files
    finally:
        if created_files:
            for file in created_files:
                file.unlink()
        folder_absolute_path.rmdir()


def _create_dir_if_not_exist_returning_abs_path(dir_name: str):
    folder_path = pathlib.Path(dir_name)
    pathlib.Path(dir_name).mkdir(exist_ok=True)

    return folder_path.resolve()
