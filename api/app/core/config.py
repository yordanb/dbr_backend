from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    # Secondary DB (db_mte)
    MTE_DB_HOST: str = "postgres"
    MTE_DB_PORT: int = 5432
    MTE_DB_NAME: str = "db_mte"
    MTE_DB_USER: str = "postgres"
    MTE_DB_PASSWORD: str = "postgres123"


settings = Settings()
