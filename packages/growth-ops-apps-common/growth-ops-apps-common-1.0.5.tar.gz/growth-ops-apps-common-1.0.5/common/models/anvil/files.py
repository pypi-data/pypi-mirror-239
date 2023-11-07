from pydantic import BaseModel


class UploadFileRequestModel(BaseModel):
    portal_id: int
    object_type: str
    hs_object_id: int
    property_name: str
    file: str
    options: dict
    file_name: str
