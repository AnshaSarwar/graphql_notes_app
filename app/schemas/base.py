from pydantic import BaseModel, ConfigDict

# Base Pydantic schema with default configuration for all response models
class BaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
