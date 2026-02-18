from fastapi import FastAPI, Depends
from models.model import TextGenerationRequest, GeneratedTextResponse, FileInfoRequest
from models.db_models import Base
from contextlib import asynccontextmanager
from ai.gemini import GeminiAI
from database import get_db, engine
import os
from sqlalchemy.orm import Session
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

API_KEY = os.environ.get("GENAI_API_KEY", '')

def load_db():
    logger.info("Applying database schema...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database schema applied.")

def load_system_prompt() -> str:
    with open(os.path.join("ai", "system_prompt.md"), "r") as file:
        return file.read()

ai_model = GeminiAI(
    api_key=API_KEY,
    system_prompt=load_system_prompt()
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    load_db()
    yield


app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {" Welcome to the LLM Project API! "}

@app.post("/generate", response_model=GeneratedTextResponse)
def generate_text(request: TextGenerationRequest, db: Session = Depends(get_db)):
    prompt = request.prompt
    logger.info('Entered prompt', extra={"prompt": prompt})

    response = ai_model.generate_response(prompt)
    logger.info('Generated response', extra={"response": response})
    print('== generated response ==', response)

    # db.add(request.to_query_record(response))

    return GeneratedTextResponse(
        prompt=prompt,
        generated_text=response
    )
