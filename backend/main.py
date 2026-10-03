from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from backend.gemini_generator import generate_legal_document

app = FastAPI(
    title="LegalEase API",
    description="AI-powered legal document generator",
    version="1.0.0"
)


class DocumentRequest(BaseModel):
    document_type: str
    parties: str
    terms: str
    effective_date: str


@app.get("/")
def home():
    return {"message": "LegalEase API is running!"}


@app.post("/generate")
def generate_document(request: DocumentRequest):
    try:
        document = generate_legal_document(
            document_type=request.document_type,
            parties=request.parties,
            terms=request.terms,
            effective_date=request.effective_date
        )

        return {
            "success": True,
            "document": document
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )