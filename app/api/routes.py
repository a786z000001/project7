from fastapi import APIRouter
from pydantic import BaseModel
from app.core.orchestrator import run_hallucination_pipeline

router = APIRouter()


class RequestBody(BaseModel):
    response_text: str


@router.post("/score")
def score_response(body: RequestBody):
    result = run_hallucination_pipeline(body.response_text)
    return result
