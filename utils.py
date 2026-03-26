import re, json
from langchain_community.document_loaders import JSONLoader

from config import graph_instance, llm, driver

def to_relationship_name(key: str) -> str:
    """Convert camelCase property name to HAS_SNAKE_UPPER_CASE relationship."""
    # Insert underscore before uppercase letters, then uppercase everything
    snake = re.sub(r'(?<!^)(?=[A-Z])', '_', key).upper()
    return f"HAS_{snake}"

def ingest_file(file_path: str, primary_key: str):

    loader = JSONLoader(
        file_path=file_path,
        json_lines=True,
        jq_schema='.',
        text_content=False,
    )
    documents = loader.load()

    index = 1
    for doc in documents:
        print(f"Ingesting record {index}/{len(documents)}")
        json_doc = json.loads(doc.page_content)
        ingest_record(json_doc, graph_instance, primary_key)
        print(f"Ingested record {index}/{len(documents)}, remaining {len(documents) - index}")
        index += 1


def ingest_record(record, graph_instance, primary_key):

    primary_value = record[primary_key]
    node_label = primary_key[0].upper() + primary_key[1:]
    graph_instance.query(
        f"""
        MERGE (n:{node_label} {{key: $key, value: $value}})
        """,
        {"key": primary_key, "value": primary_value}
    )

    for key, value in record.items():
        if key == primary_key:
            continue
        relationship = to_relationship_name(key)
        property_label = key[0].upper() + key[1:]
        graph_instance.query(
            f"""
            MATCH (primary:{node_label} {{value: $primary_value}})
            MERGE (prop:{property_label} {{key: $key, value: $value}})
            MERGE (primary)-[:{relationship}]->(prop)
            """,
            {
                "primary_value": primary_value,
                "key": key,
                "value": str(value),
            }
        )

def query_neo4j(query_prompt: str):
    result = driver.execute_query("MATCH (n) RETURN DISTINCT labels(n) AS labels")
    labels = [rec["labels"][0] for rec in result.records]
    flattended_labels = ", ".join(labels)

    cypher_query = llm.invoke(
        f"You are a helpful assistant for translating natural language queries \
        into Cypher queries. Given the following natural language query, \
        generate a Cypher query that can be executed against a Neo4j graph database. \
        Here is the natural language query: '{query_prompt}'.  \
        Node Labels available in the database are: {flattended_labels}. \
        All values are strings. \
        Please provide only the Cypher query as the output. \
        Rules you MUST follow: \
            1. Always use directed relationships: (a)-[r]->(b), never undirected (a)-[r]-() \
            2. Always RETURN all three: the anchor node, relationship, AND the connected node (a, r, b) \
            3. Use OPTIONAL MATCH for relationships so the anchor node is returned even with no connections \
            4. Please provide only the Cypher query as output, no explanations or notes."
    )
    modified_cypher_query = cypher_query.replace('```cypher', '').replace('```', '').replace('\n', '').strip()
    query_result = driver.execute_query(modified_cypher_query)
    return llm.invoke(
        f"You are a helpful assistant for summarizing Neo4j query results. Given the following Cypher query and its result, provide a concise summary of the information retrieved. Here is the Cypher query: '{modified_cypher_query}' and its result: '{query_result}'. Please provide a brief summary of the key insights from this query result."
    )
