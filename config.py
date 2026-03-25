import os
from dotenv import load_dotenv
from langchain_neo4j import Neo4jGraph
from langchain_openai import OpenAI
from neo4j import GraphDatabase

load_dotenv()

url=os.getenv("url")
username=os.getenv("username")
password=os.getenv("password")
database=os.getenv("database")

graph_instance = Neo4jGraph(
    database=database,
    url=url,
    username=username,
    password=password
)

llm = OpenAI(model="gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"), temperature=0)

driver = GraphDatabase.driver(uri=url, auth=(username, password))

try:
    driver.verify_connectivity()
    print("Successfully connected to Neo4j database.")
except Exception as e:
    print(f"Failed to connect to Neo4j database: {e}")
    driver.close()
    raise e