from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
import os

load_dotenv()

url = URL.create(
    drivername="postgresql",
    username=os.getenv('PGSQL_USER'),
    password=os.getenv('PGSQL_PASS'),
    host=os.getenv('PGSQL_HOST'),
    database=os.getenv('PGSQL_DB'),
    port=os.getenv('PGSQL_PORT')
)

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()