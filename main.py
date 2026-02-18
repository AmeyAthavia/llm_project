from fastapi import FastAPI, Depends, UploadFile
from models import model as Models 
from models.db_models import Base
from contextlib import asynccontextmanager
from ai.gemini import GeminiAI
from database import get_db, engine
import os
from api.api import API
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

@app.post("/generate", response_model=Models.GeneratedTextResponse)
def generate_text(request: Models.TextGenerationRequest, db: Session = Depends(get_db)):
    prompt = request.prompt
    logger.info('Entered prompt', extra={"prompt": prompt})

    response = ai_model.generate_response(prompt)
    logger.info('Generated response', extra={"response": response})
    print('== generated response ==', response)

    # db.add(request.to_query_record(response))

    return Models.GeneratedTextResponse(
        prompt=prompt,
        generated_text=response
    )

@app.post("/file", response_model=Models.FileDataResponse)
def get_file_info(request: Models.FileInfoRequest, db: Session = Depends(get_db)):
    file_name = request.file_name
    logger.info('Received file info request', extra={"file_name": file_name})
    response = API.get_files_data(db, file_name)
    logger.info('Retrieved file info', extra={"file_name": file_name, "response": response})
    # Implement logic to retrieve and return file information based on the file_name
    return Models.FileDataResponse(files=response['files'])

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile, db: Session = Depends(get_db)):
    #saving data to db
    response  = API.add_new_file(file, db)
    logger.info('Received file upload', extra={"file_name": file.filename})
    return response