from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
DATABASE_URL = "postgresql://postgres:@localhost:5432/dbmetro"
engine = create_engine(DATABASE_URL)
local_session = sessionmaker(bind=engine)
Base = declarative_base()