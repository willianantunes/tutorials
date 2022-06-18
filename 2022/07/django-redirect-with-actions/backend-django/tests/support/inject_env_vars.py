import pathlib

import pytest

from dotenv import load_dotenv

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent.parent


@pytest.hookimpl(tryfirst=True)
def pytest_load_initial_conftests(args, early_config, parser):
    load_dotenv(BASE_DIR.joinpath(".env.development"))
