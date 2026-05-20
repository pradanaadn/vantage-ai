from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "Vantage AI"

    # Firebase Settings
    FIREBASE_PROJECT_ID: str = "vantage-ai-default"
    FIREBASE_STORAGE_BUCKET: str | None = None
    USE_FIREBASE_EMULATORS: bool = True
    FIREBASE_SERVICE_ACCOUNT_PATH: str | None = None
    
    # Emulator Hosts
    FIRESTORE_EMULATOR_HOST: str = "127.0.0.1:8080"
    FIREBASE_AUTH_EMULATOR_HOST: str = "127.0.0.1:9099"
    FIREBASE_STORAGE_EMULATOR_HOST: str = "127.0.0.1:9199"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
