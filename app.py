from fastapi import FastAPI
from pydantic import BaseModel

from script import run_ingestion_script
from controller import query

app = FastAPI()

class QueryNeo4jRequest(BaseModel):
    query_prompt: str


@app.get("/script")
def ingest():
    run_ingestion_script()
    return {"message": "Script executed successfully"}

@app.post("/query")
def queryPrompt(payload: QueryNeo4jRequest):
    response = query(payload.query_prompt)
    return {"response": response}