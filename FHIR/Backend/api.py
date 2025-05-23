from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from nlp_mapper import parse_query, simulate_fhir_response

app = FastAPI(
    title="AI on FHIR - NLP API",
    description="Convert natural language queries into simulated FHIR API responses.",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "API is live!"}

@app.post("/parse-query")
def parse_query_endpoint(request: QueryRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query is empty.")
    
    parsed = parse_query(request.query)
    response = simulate_fhir_response(parsed)
    
    return {
        "query": request.query,
        "parsed": parsed,
        "fhirResponse": response
    }
