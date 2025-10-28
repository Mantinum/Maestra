"""Application FastAPI simulant l'IA corse pour A Maestra."""
from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI(title="A Maestra API", description="API simulant l'assistante corse.")


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


SIMULATED_RESPONSES: dict[Mode, str] = {
    Mode.TALK: "TODO: réponse corse ici (mode conversation)",
    Mode.TRANSLATE: "TODO: traduction corse/français ici",
    Mode.CORRECT: "TODO: correction et explication en corse ici",
    Mode.EXPLAIN: "TODO: explication de règle en corse/français ici",
}


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest) -> ChatResponse:
    """Endpoint principal permettant de discuter avec l'IA simulée.

    Pour l'instant, les réponses sont statiques en attendant le branchement du modèle.
    """

    simulated_answer = SIMULATED_RESPONSES.get(payload.mode)
    if not simulated_answer:
        raise HTTPException(status_code=400, detail="Mode non pris en charge")
    return ChatResponse(answer=simulated_answer)


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    """Permet de vérifier que l'API est vivante."""

    return {"status": "ok"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
