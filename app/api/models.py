from pydantic import BaseModel

class NetcdfData(BaseModel):
    filepath: str


