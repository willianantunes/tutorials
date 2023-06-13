import pathlib

from dotenv import load_dotenv

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR.joinpath(".env.development"))
