from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MAX_ORDER_QUANTITY: int = 100


settings = Settings()
