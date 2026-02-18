from sqlalchemy import Column, Integer, String, UUID, JSON
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"
    
    id = Column(UUID, primary_key=True, index=True)
    username = Column(String, unique=True)
    created_at = Column(String)

    def to_dict(self):
        return {
            "id": str(self.id),
            "username": self.username,
            "created_at": self.created_at
        }

class SchemaModel(Base):
    __tablename__ = "schema"
    
    id = Column(UUID, primary_key=True)
    name = Column(String, index=True)
    created_at = Column(String)
    file_path = Column(String)

    def to_dict(self):
        return {
            "id": str(self.id),
            "name": self.name,
            "created_at": self.created_at,
            "file_path": self.file_path
        }

class QueryRecordModel(Base):
    __tablename__ = "query_records"
    
    id = Column(UUID, primary_key=True)
    schema_id = Column(UUID, index=True)
    query_text = Column(String)
    response_text = Column(String)
    created_at = Column(String)
    user_id = Column(UUID, index=True)

    def to_dict(self):
        return {
            "id": str(self.id),
            "schema_id": str(self.schema_id),
            "query_text": self.query_text,
            "response_text": self.response_text,
            "created_at": self.created_at,
            "user_id": str(self.user_id)
        }

class FileUploadData(Base):
    __tablename__ = "file_uploads"
    
    id = Column(UUID, primary_key=True)
    file_name = Column(String, index=True)
    top_rows = Column(JSON)
    created_at = Column(String)

    def to_dict(self):
        return {
            "id": str(self.id),
            "file_name": self.file_name,
            "top_rows": self.top_rows,
            "created_at": self.created_at
        }
    