from typing import Optional
from pydantic import BaseModel, Field


class AppicRequestSchema(BaseModel):
    prompt: str


class AppicResponseSchema(BaseModel):
    name: Optional[str] = Field(default=None, description="Name of the component.")
    component: Optional[str] = Field(default=None, description="Component code.")
