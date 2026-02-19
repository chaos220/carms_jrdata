# scripts/load_lookup.py
import pandas as pd
from sqlalchemy.orm import sessionmaker
from models import Discipline, School, Base
from sqlalchemy import create_engine
import os, dotenv

dotenv.load_dotenv()
engine = create_engine(os.getenv('DB_URL'))
Session = sessionmaker(bind=engine)

def upsert(df, Model, pk_col):
    # Insert rows that don’t already exist
    sess = Session()
    for _, row in df.iterrows():
        exists = sess.query(Model).filter(getattr(Model, pk_col)==row[pk_col]).first()
        if not exists:
            sess.add(Model(**row.to_dict()))
    sess.commit()
    sess.close()

# ------------------------------------------------------------------
# Discipline lookup
disc_df = pd.read_excel('data/1503_discipline.xlsx')   # columns: discipline_id, discipline
disc_df = disc_df.rename(columns={'discipline_id':'id', 'discipline':'name'})
upsert(disc_df, Discipline, 'id')

# ------------------------------------------------------------------
# School lookup (from program master sheet)
master = pd.read_excel('data/1503_program_master.xlsx')
school_df = master[['school_id','school_name']].drop_duplicates()
school_df = school_df.rename(columns={'school_id':'id', 'school_name':'name'})
upsert(school_df, School, 'id')

print("load_lookups.py --> Lookup tables loaded")