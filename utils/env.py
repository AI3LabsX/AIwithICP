from os import path
from sys import exit as sys_exit
from typing import Any

from environs import Env, EnvError
from langchain.chat_models import ChatOpenAI

from utils.config import ENV_FILE
from utils.logger import logger


class Environment:

    def __init__(self, path_to_env_file: str) -> None:
        if not path.exists(path_to_env_file):
            logger.critical("Env file not found", path_to_env_file)
            sys_exit(1)

        self._env: Env = Env()
        self._env.read_env(path=path_to_env_file, recurse=False)

    def _get_env_var(self, var_name: str) -> str:
        try:
            return self._env.str(var_name)
        except EnvError as exc:
            logger.critical(f"{var_name} not found", repr(exc))
            sys_exit(repr(exc))

    def get_openai_api(self) -> str:
        return self._get_env_var("OPENAI_API_KEY")

    def get_google_search(self) -> str:
        return self._get_env_var("GOOGLE_SEARCH_API")


class Config:
    def __init__(self):
        self._openai_api_key = None
        self._google_api = None

    @property
    def get_google_api(self) -> str:
        self._google_api = env.get_google_search()
        return self._google_api

    @property
    def OPENAI_MODEL_NAME(self) -> str:
        return "gpt-3.5-turbo"

    @property
    def model(self) -> Any:  # Replace Any with the actual type of ChatOpenAI
        return ChatOpenAI(model_name=self.OPENAI_MODEL_NAME, openai_api_key=self.openai_api_key)

    @property
    def openai_api_key(self) -> str:
        if self._openai_api_key is None:
            self._openai_api_key = env.get_openai_api()
        return self._openai_api_key


env: Environment = Environment(path_to_env_file=ENV_FILE)
