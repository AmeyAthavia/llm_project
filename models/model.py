from pydantic import BaseModel
from fastapi import UploadFile


class TextGenerationRequest(BaseModel):
    prompt: str

class GeneratedTextResponse(BaseModel):
    prompt: str
    generated_text: str

class FileInfoRequest(BaseModel):
    file_name: str = None

class GetFileUpload(BaseModel):
    file_name: str
    description: str
    files: UploadFile

class FileDataResponse(BaseModel):
    files: str