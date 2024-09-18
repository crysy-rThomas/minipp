# Create Graph Knowledge
import os

from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph

load_dotenv()
KG_URL = os.getenv("KG_URL")
KG_USER = os.getenv("KG_USER")
KG_PSSWD = os.getenv("KG_PSSWD")

kg = Neo4jGraph(KG_URL, username=KG_USER, password=KG_PSSWD)
