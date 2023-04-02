import tomllib
from pathlib import Path
from typing import Any, Tuple, Callable, Dict

from pydantic import BaseSettings, BaseModel, ValidationError

SETTINGS_PATH = Path(__file__).parent.parent / "settings.toml"


class SettingsError(Exception):
    pass


class SettingsFileNotFoundError(SettingsError):
    pass


class SettingParsingError(SettingsError):
    pass


class SettingsValidationError(SettingsError):
    pass


class Settings(BaseModel):
    secret_key: str


def load_settings() -> Settings:
    if not SETTINGS_PATH.is_file():
        raise SettingsFileNotFoundError()

    with SETTINGS_PATH.open("r") as file:
        raw_toml = file.read()

    try:
        parsed_toml = tomllib.loads(raw_toml)
    except tomllib.TOMLDecodeError:
        raise SettingParsingError()

    try:
        validated_model = Settings.parse_obj(parsed_toml)
    except ValidationError as error:
        raise SettingsValidationError(str(error))

    return validated_model
