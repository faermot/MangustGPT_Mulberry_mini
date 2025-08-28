from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from typing import List


class Settings(BaseSettings):
    bot_token: SecretStr
    admin_ids: str
    db_path: str
    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

    @property
    def admin_ids_list(self) -> List[int]:
        return list(map(int, self.admin_ids.split(',')))


config = Settings()
