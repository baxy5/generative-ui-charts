from typing import Optional
from pydantic import BaseModel, Field


class RechartRequestSchema(BaseModel):
    prompt: str


class RechartComponentResponseSchema(BaseModel):
    name: Optional[str] = Field(default=None, description="Name of the component.")
    component: Optional[str] = Field(default=None, description="Component code.")
    rechartComponents: Optional[list[str]] = Field(
        default=None, description="List of rechart components used in the component."
    )
