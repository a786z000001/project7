from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    OPENAI_API_KEY: str
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
    APP_NAME: str = "HalluGuard"
    APP_VERSION: str = "1.0.0"

    CONTRADICTION_THRESHOLD: float = 0.75
    UNKNOWN_THRESHOLD: float = 0.40

    WEIGHT_CONTRADICTION: float = 0.5
    WEIGHT_UNKNOWN: float = 0.2
    WEIGHT_ENTROPY: float = 0.2
    WEIGHT_VARIANCE: float = 0.1

    RETRIEVAL_TIMEOUT: int = 5
    MAX_CLAIMS: int = 20


settings = Settings()
