import os

class Config:
    KAFKA_HOST = os.environ.get("KAFKA_HOST", "localhost")
    KAFKA_PORT = os.environ.get("KAFKA_PORT", "9092")
