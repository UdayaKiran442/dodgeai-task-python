from utils import query_neo4j

def query(query_prompt: str):
    return query_neo4j(query_prompt)
