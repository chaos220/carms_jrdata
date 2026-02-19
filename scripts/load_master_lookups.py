# load_master_programs.py
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from models import Program, Discipline, School
import os, dotenv, tqdm

dotenv.load_dotenv()
engine = create_engine(os.getenv('DB_URL'))
Session = sessionmaker(bind=engine)

master = pd.read_excel('data/1503_program_master.xlsx')
# rename columns to match model
master = master.rename(columns={
    'discipline_id':'discipline_id',
    'discipline_name':'discipline_name',
    'school_id':'school_id',
    'school_name':'school_name',
    'program_stream_id':'stream_id',
    'program_stream_name':'stream_name',
    'program_site':'site',
    'program_name':'name',
    'program_url':'url'
})

sess = Session()
for _, row in tqdm.tqdm(master.iterrows(), total=len(master)):
    prog = Program(
        discipline_id=row['discipline_id'],
        school_id=row['school_id'],
        stream_id=row['stream_id'],
        stream_name=row['stream_name'],
        site=row['site'],
        name=row['name'],
        url=row['url']
    )
    sess.add(prog)
sess.commit()
sess.close()
print("load_master_lookups.py --> Master program rows inserted")