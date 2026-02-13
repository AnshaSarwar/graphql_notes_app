from pydantic import BaseModel, ConfigDict

class BaseSchema(BaseModel):
    """
    Base Pydantic schema with default configuration for all response models.
    """
    model_config = ConfigDict(from_attributes=True)
