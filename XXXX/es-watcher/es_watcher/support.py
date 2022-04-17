import os

from distutils.util import strtobool


def getenv_or_raise_exception(varname: str) -> str:
    env = os.getenv(varname)

    if env is None:
        raise EnvironmentError(f"Environment variable {varname} is not set!")

    return env


def eval_env_as_boolean(varname, standard_value) -> bool:
    return bool(strtobool(os.getenv(varname, str(standard_value))))
