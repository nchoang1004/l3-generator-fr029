from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    INVENTORY_URL: str = "https://inventory.example.com/reserve"
    PAYMENT_URL: str = "https://pay.example.com/charge"
    DATABASE_URL: str = "sqlite:///./orders.db"


settings = Settings()
