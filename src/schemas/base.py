from pydantic import BaseModel, ConfigDict
from datetime import date


class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
