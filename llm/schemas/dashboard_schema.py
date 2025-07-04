from typing import List, Optional, TypedDict
from pydantic import BaseModel, Field


class LayoutRequestSchema(BaseModel):
    """Schema for API "layout" phase request."""

    query: str = Field(description="User query.")
    data: str = Field(description="Provided dataset by the user.")
    phase: str = Field(
        default="layout",
        description="Phase identifier for the nodes of the Agent. Either 'layout' or 'final'",
    )


class FinalRequestSchema(BaseModel):
    """Schema for API "final" phase request."""

    phase: str = Field(
        default="final",
        description="Phase identifier for the nodes of the Agent. Either 'layout' or 'final'",
    )
    layout_id: str = Field(
        description="Selected layout by the user. Only needed in 'final' node."
    )


class LayoutsResponse(BaseModel):
    """Schema for "layouts" in LayoutResponseSchema."""

    url: str = Field(description="R2 public url for displaying in Iframe.")
    layout_id: str


class LayoutResponseSchema(BaseModel):
    """Schema for API "layout" phase response."""

    layouts: List[LayoutsResponse] = Field(description="Information for each layout.")


class FinalResponseSchema(BaseModel):
    """Schema for API "final" phase response."""

    url: str = Field(description="R2 public url for final dashboard.")


class Layout(BaseModel):
    layout_id: str
    page_title: str
    html: str
    css: str
    js: str


class LayoutNode(BaseModel):
    """Schema for the Layout generation node of the Agent workflow."""

    layouts: List[Layout] = Field(description="Three layouts.")


class FinalNode(BaseModel):
    """Schema for the final generation node of the Agent workflow."""

    layout: Layout


class AgentState(TypedDict):
    """State schema of the Agent workflow."""

    query: str = Field(description="User query.")
    data: str = Field(description="Provided dataset by the user.")
    ui_descriptor: str = Field(description="Descriptors of the UI/DS elements.")
    design_system: str = Field(
        description="CSS classes and descriptors of a design system."
    )
    phase: str = Field(
        description="Phase identifier for the nodes of the Agent. Either 'layout' or 'final'"
    )
    selected_layout: Layout = Field(description="Selected layout by the user.")
    layouts: List[Layout] = Field(description="The three layouts for service.")
    final: Layout = Field(description="Final layout for service.")
