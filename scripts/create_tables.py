# scripts/create_tables.py

import os, dotenv
from sqlalchemy import create_engine
from models import Base
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent.parent / ".env"   # project‑root/.env
load_dotenv(dotenv_path=env_path)

# Build SQLAlchemy URL
# Prefer the explicit DB_URL if it exists, otherwise compose it
DB_URL = os.getenv(
    "DB_URL",
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DB_URL, echo=True) 
Base.metadata.create_all(engine)

print("create_tables.py executed --> Tables created")