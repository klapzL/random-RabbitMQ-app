from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    RMQ_USER: str = Field(validation_alias="RABBITMQ_DEFAULT_USER")
    RMQ_PASSWORD: str = Field(validation_alias="RABBITMQ_DEFAULT_PASS")
    RMQ_HOST: str = Field(validation_alias="RABBITMQ_HOST_NAME")
    RMQ_PORT: int = Field(validation_alias="RABBITMQ_PORT")
    RMQ_QUEUE: str = Field(validation_alias="RABBITMQ_QUEUE")

    @property
    def RMQ_URL(self):
        return f"amqp://{self.RMQ_USER}:{self.RMQ_PASSWORD}@{self.RMQ_HOST}:{self.RMQ_PORT}/"


settings = Settings()
