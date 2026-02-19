# load_program_pages.py
import json, pathlib, tqdm
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine, select
from models import Program
import os, dotenv

dotenv.load_dotenv()
engine = create_engine(os.getenv('DB_URL'))
Session = sessionmaker(bind=engine)

# Load JSON – it is a list of dicts
json_path = pathlib.Path('data/1503_program_descriptions.json')
pages = json.loads(json_path.read_text())

sess = Session()
for rec in tqdm.tqdm(pages):
    # Grab the URL that belongs to this page – it is stored in metadata.source
    url = rec.get('metadata', {}).get('source')
    if not url:
        continue

    # Find the program row that has this exact URL
    prog = sess.execute(
        select(Program).where(Program.url == url)
    ).scalar_one_or_none()

    if prog:
        prog.raw_html = rec['page_content']
    else:
        # If you ever see a mismatch, print it – helps catch bad data early
        print("No program row for URL:", url)

sess.commit()
sess.close()
print("load_program_pages.py --> HTML pages attached")