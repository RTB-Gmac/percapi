from fastapi import FastAPI
from perc import Percolator
from pydantic import BaseModel

class QueryRequest(BaseModel):
    query: list[str]
    category: str
    minimum_match: int
    unique_term_count: bool

class DocumentRequest(BaseModel):
    document: str

app = FastAPI()
percolator = Percolator()

@app.post("/add_query")
def add_query(request: QueryRequest):
    percolator.add_query(request.query, request.category, request.minimum_match, request.unique_term_count)
    return {"message": "Query added successfully"}

@app.post("/percolate")
def percolate(request: DocumentRequest):
    matches = percolator.percolate(request.document)
    return {"matches": matches}

@app.get("/finalize")
def finalize():
    percolator.finalize()
    return {"automation made / finalized"}