import os


class Tokens:
    POSTGRESQL_USER = os.getenv('POSTGRESQL_USER')
    POSTGRESQL_PASSWORD = os.getenv('POSTGRESQL_PASSWORD')
    POSTGRESQL_DATABASE = os.getenv('POSTGRESQL_DATABASE')

    REDIS_HOST = os.getenv('REDIS_HOST')
    DOCKER_POSTGRESQL_HOST = os.getenv('DOCKER_POSTGRESQL_HOST')
    DEFAULT_POSTGRESQL_HOST = os.getenv('DEFAULT_POSTGRESQL_HOST')

    RABBITMQ_HOST = os.getenv('RABBITMQ_HOST')
    RABBITMQ_USERNAME = os.getenv('RABBITMQ_USERNAME')
    RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD')

    SQLALCHEMY_POSTGRESQL_URL = f'postgresql+asyncpg://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}' \
                                f'@{DOCKER_POSTGRESQL_HOST}/{POSTGRESQL_DATABASE}'
    ALEMBIC_POSTGRESQL_URL = f'postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}' \
                             f'@{DEFAULT_POSTGRESQL_HOST}/{POSTGRESQL_DATABASE}'
    DB_BACKUPER_POSTGRESQL_URL = f'postgresql://{POSTGRESQL_USER}:{POSTGRESQL_PASSWORD}' \
                                 f'@{DOCKER_POSTGRESQL_HOST}/{POSTGRESQL_DATABASE}'
