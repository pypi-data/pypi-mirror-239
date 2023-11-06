import json
import os
from pathlib import Path
from typing import Any, Dict, List, Tuple, Type

import yaml
from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
)

ROOT_PACKAGE_NAME = __package__.split(".")[0]
ACTIVE_PROFILE = ROOT_PACKAGE_NAME + "_active_profile"


class BaseConfigSettingsSource(PydanticBaseSettingsSource):
    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        return value

    def __call__(self) -> Dict[str, Any]:
        d: Dict[str, Any] = {}

        for field_name, field in self.settings_cls.model_fields.items():
            field_value, field_key, value_is_complex = self.get_field_value(
                field, field_name
            )
            field_value = self.prepare_field_value(
                field_name, field, field_value, value_is_complex
            )
            if field_value is not None:
                d[field_key] = field_value

        return d


class JsonConfigSettingsSource(BaseConfigSettingsSource):
    """
    A simple settings source class that loads variables from a JSON file
    at the project's root.

    Here we happen to choose to use the `env_file_encoding` from Config
    when reading `config.json`
    """

    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:
        encoding = self.config.get("env_file_encoding")
        configFilePath = Path(self.config.get("config_file_folder"), "config.json")
        file_content_json = {}
        if os.path.exists(configFilePath):
            file_content_json = json.loads(configFilePath.read_text(encoding))
        field_value = file_content_json.get(field_name)
        return field_value, field_name, False


class YamlConfigSettingsSource(BaseConfigSettingsSource):
    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:
        encoding = self.config.get("env_file_encoding")
        configFilePath = Path(self.config.get("config_file_folder"), "config.yaml")
        file_content_json = {}
        if os.path.exists(configFilePath):
            file_content_json = (
                yaml.load(
                    configFilePath.read_text(encoding), Loader=yaml.loader.FullLoader
                )
                or {}
            )
        field_value = file_content_json.get(field_name)
        return field_value, field_name, False


class ActiveProfileSettingSource(BaseConfigSettingsSource):
    def get_field_value(
        self, field: FieldInfo, field_name: str
    ) -> Tuple[Any, str, bool]:
        encoding = self.config.get("env_file_encoding")
        activeProfile = self.config.get("active_profile")
        configFilePath = Path(
            self.config.get("config_file_folder"), f"config_{ activeProfile }.yaml"
        )
        file_content_json = {}
        if os.path.exists(configFilePath):
            file_content_json = (
                yaml.load(
                    configFilePath.read_text(encoding), Loader=yaml.loader.FullLoader
                )
                or {}
            )
        field_value = file_content_json.get(field_name)
        return field_value, field_name, False


def check_config_file_folder():
    config_file_folder_list = [
        Path(".").joinpath("config"),
        Path(f"/etc/{ROOT_PACKAGE_NAME}"),
    ]
    for config_file_folder in config_file_folder_list:
        if config_file_folder.exists():
            return config_file_folder
    raise FileNotFoundError("配置文件不存在")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file_encoding="utf-8",
        config_file_folder=check_config_file_folder(),
        active_profile=os.getenv(ACTIVE_PROFILE),
    )
    # 在此添加需要的配置项
    package_name: str = ROOT_PACKAGE_NAME
    mysql_url: str

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            ActiveProfileSettingSource(settings_cls),
            YamlConfigSettingsSource(settings_cls),
            JsonConfigSettingsSource(settings_cls),
            env_settings,
            file_secret_settings,
        )


SETTING = Settings()

if __name__ == "__main__":
    print(SETTING)
