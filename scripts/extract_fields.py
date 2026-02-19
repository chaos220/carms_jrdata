# scripts/extract_fields.py
import os
import re
from pathlib import Path

import pandas as pd
from sqlalchemy import create_engine, update, text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=env_path)

DB_URL = os.getenv(
    "DB_URL",
    f"postgresql+psycopg2://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@db:5432/{os.getenv('POSTGRES_DB')}"
)

engine = create_engine(DB_URL, echo=False)
Session = sessionmaker(bind=engine)


def extract_fields(html: str) -> dict:
    out = {}

    # ---- quota ---------------------------------------------------------
    m = re.search(r'Approximate Quota.*?<h2[^>]*>\s*&nbsp;(\d+)', html, re.S)
    out["quota"] = int(m.group(1)) if m else None

    # ---- program director name -----------------------------------------
    m = re.search(r'Program Director</label>\s*<span>\s*([^<]+)', html, re.S)
    out["director_name"] = m.group(1).strip() if m else None

    # ---- director e‑mail ------------------------------------------------
    m = re.search(r'mailto:([^"]+)', html, re.S)
    out["director_email"] = m.group(1).strip() if m else None

    # ---- interview dates (may be multiple) -----------------------------
    dates = re.findall(r'<li>\s*([A-Za-z]+\s+\d{1,2},\s*\d{4})\s*</li>', html)
    out["interview_dates"] = ", ".join(dates) if dates else None

    # ---- accreditation status ------------------------------------------
    m = re.search(r'Accreditation status\s*:\s*(\w+)', html, re.S)
    out["accreditation"] = m.group(1).strip() if m else None

    return out


# Ensure columns exist
with engine.begin() as conn:
    conn.execute(
        text(
            """
            ALTER TABLE program
            ADD COLUMN IF NOT EXISTS quota INTEGER,
            ADD COLUMN IF NOT EXISTS director_name TEXT,
            ADD COLUMN IF NOT EXISTS director_email TEXT,
            ADD COLUMN IF NOT EXISTS interview_dates TEXT,
            ADD COLUMN IF NOT EXISTS accreditation TEXT;
            """
        )
    )

session = Session()

# Pull only rows that actually have HTML stored
program_rows = session.execute(
    text("SELECT id, raw_html FROM program WHERE raw_html IS NOT NULL")
).fetchall()


from models import Program   # <-- make sure this import is AFTER the engine is created

for prog_id, raw_html in program_rows:
    if not raw_html:
        continue

    fields = extract_fields(raw_html)

    payload = {k: v for k, v in fields.items() if v is not None}

    # Skip rows where nothing was extracted (payload empty)
    if not payload:
        continue

    stmt = (
        update(Program)                     # correct subject table
        .where(Program.id == prog_id)
        .values(**payload)
    )

    session.execute(stmt)

session.commit()
session.close()

print("extract_fields.py --> Structured fields extracted and stored in the DB")