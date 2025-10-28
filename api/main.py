"""Application FastAPI simulant l'IA corse pour A Maestra."""
from enum import Enum

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


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    """Permet de vérifier que l'API est vivante."""

    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
