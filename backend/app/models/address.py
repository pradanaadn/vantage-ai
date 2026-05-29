from pydantic import BaseModel

class Address(BaseModel):
    jalan: str
    desa_kelurahan: str
    kecamatan: str
    kota: str
    provinsi: str
    kode_pos: str
    
class GoogleMapsURL(BaseModel):
    url: str
    name: str
    address: Address | None = None
    latitude: float
    longitude: float