# db.py
from contextlib import contextmanager
import os

from dotenv import load_dotenv
from neo4j import GraphDatabase
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

load_dotenv()

SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Create the database engine
engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_size=100, max_overflow=0)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for declarative models
Base = declarative_base()


# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Create Graph Knowledge
KG_URL = os.getenv("KG_URL")
KG_USER = os.getenv("KG_USER")
KG_PSSWD = os.getenv("KG_PSSWD")

kg_driver = GraphDatabase.driver(KG_URL, auth=(KG_USER, KG_PSSWD))


@contextmanager
def get_kg():
    kg = kg_driver.session()
    try:
        yield kg
    finally:
        kg.close()
