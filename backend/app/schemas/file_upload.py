from pydantic import BaseModel, Field

class FileUpload(BaseModel):
    filename: str = Field(..., description="Nama file yang diunggah")
    content_type: str = Field(..., description="Tipe konten file")
    data: bytes = Field(..., description="Data file dalam bentuk byte")
    