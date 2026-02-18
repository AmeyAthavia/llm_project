from models import db_models
from datetime import datetime
import os, json
from sqlalchemy import select
from uuid import uuid4
import pandas as pd


class API:
    @staticmethod
    def add_new_file(file, db):
        file_name = file.filename
        if file_name.split('.')[-1] not in ['csv', 'xlsx']:
            return {"error": "Unsupported file type. Only CSV and XLSX are allowed."}
        
        if file_name.endswith('.csv'):
            data = pd.read_csv(file.file)
            data.to_csv(os.path.join("./uploads", file_name), index=False)
        else:
            data = pd.read_excel(file.file)
            data.to_excel(os.path.join("./uploads", file_name), index=False)

        data_preview = data.head(n=10).to_dict(orient='records')

        db.add(db_models.SchemaModel(
            id = uuid4(),
            name=file.filename,
            created_at=datetime.now().isoformat(),
            file_path=os.path.join("./uploads", file.filename)
        ))

        db.add(db_models.FileUploadData(
            id = uuid4(),
            file_name=file.filename,
            top_rows=data_preview,
            created_at=datetime.now().isoformat()
        ))

        db.commit()
        return {"message": "File uploaded and processed successfully.", "file_name": file.filename, "numberOfRows": len(data)}
    
    @staticmethod
    def get_files_data(db, file_name=None):
        print('== file_name from request ==', file_name)
        if file_name != "":
            query = select(db_models.FileUploadData).where(db_models.FileUploadData.file_name == file_name)
            data = db.scalars(query).first()
        else:
            print('==== here ====')
            query = select(db_models.FileUploadData).order_by(db_models.FileUploadData.created_at.desc())
            data = db.scalars(query).all()
        print('== all files from db ==', data)
        data = json.dumps([file.to_dict() for file in data])
        print('== all files in json ==', data)
        return {'files': data}