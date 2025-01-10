import os
from dotenv import load_dotenv


load_dotenv()


if os.path.exists('/.dockerenv') or os.path.exists('/proc/self/cgroup'):
    DB_HOST = os.environ.get("DB_HOST_DOCKER")
    DB_PORT = os.environ.get("DB_PORT_DOCKER")
else:
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT")

DATABASE_URL = f'postgresql+asyncpg://{os.environ.get("DB_USER")}:{os.environ.get("DB_PASS")}@{DB_HOST}:{DB_PORT}/{os.environ.get("DB_NAME")}'
