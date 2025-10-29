"""Application FastAPI simulant l'IA corse pour A Maestra."""
from enum import Enum
import json
import time
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="A Maestra API", description="API simulant l'assistante corse.")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Mode(str, Enum):
    """Modes pris en charge par l'API."""

    TALK = "talk"
    TRANSLATE = "translate"
    CORRECT = "correct"
    EXPLAIN = "explain"


class ChatRequest(BaseModel):
    """Schéma de requête pour l'endpoint /chat."""

    mode: Mode = Field(..., description="Mode d'interaction demandé")
    input_text: str = Field(..., min_length=1, description="Texte fourni par l'utilisateur")


class ChatResponse(BaseModel):
    """Schéma de réponse pour l'endpoint /chat."""

    answer: str


class ContributionRequest(BaseModel):
    """Schéma d'entrée pour collecter les propositions de la communauté."""

    direction: str
    source_text: str
    target_text: str
    notes: str | None = None


DATA_DIRECTORY = Path(__file__).resolve().parent.parent / "data"
CONTRIBUTIONS_FILE = DATA_DIRECTORY / "contributions_pending.jsonl"


def construire_reponse_simulee(payload: ChatRequest) -> str:
    """Fabrique une réponse textuelle en fonction du mode demandé."""

    if payload.mode == Mode.TALK:
        return f"Bonghjornu 🙂 Ti rispondu in corsu (démo) : {payload.input_text}"
    if payload.mode == Mode.TRANSLATE:
        return f"Traduction simulée : {payload.input_text}"
    if payload.mode == Mode.CORRECT:
        return (
            "Correction simulée : "
            f"{payload.input_text}"
            " | Spiegazione: (démo)"
        )
    if payload.mode == Mode.EXPLAIN:
        return "Explication simulée d'une règle de langue corse."
    raise HTTPException(status_code=400, detail="Mode non pris en charge")


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest) -> ChatResponse:
    """Endpoint principal permettant de discuter avec l'IA simulée.

    Pour l'instant, les réponses sont statiques en attendant le branchement du modèle.
    """

    simulated_answer = construire_reponse_simulee(payload)
    return ChatResponse(answer=simulated_answer)


@app.post("/contribute")
async def contribute(payload: ContributionRequest) -> dict[str, str]:
    """Enregistre une proposition de contribution linguistique utilisateur."""

    DATA_DIRECTORY.mkdir(exist_ok=True)
    line = {
        "direction": payload.direction,
        "source_text": payload.source_text,
        "target_text": payload.target_text,
        "notes": payload.notes,
        "timestamp": time.time(),
    }

    with CONTRIBUTIONS_FILE.open("a", encoding="utf-8") as file:
        file.write(json.dumps(line, ensure_ascii=False) + "\n")

    return {"status": "ok", "message": "Merci pour ta contribution ❤️"}


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    """Permet de vérifier que l'API est vivante."""

    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
