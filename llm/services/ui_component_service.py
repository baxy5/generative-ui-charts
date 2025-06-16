from typing import Annotated
from fastapi import Depends, HTTPException
from agents.ui_component_agent import (
    UiComponentAgent,
    UiComponentRequestSchema,
    UiComponentResponseSchema,
)
import json
import os
import base64


class UiComponentService:
    """Service for interacting with the UiComponent Agent."""

    def __init__(self, agent: Annotated[UiComponentAgent, Depends()]):
        self.agent = agent
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(
                current_dir, "..", "public-mock-data", "component_library.json"
            )
            with open(file_path, "r") as f:
                component_data = json.load(f)
            self.component_descriptors = json.dumps(component_data)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to load or parse component_library.json: {e}")

    async def generate_ui_component(
        self, request: UiComponentRequestSchema
    ) -> UiComponentResponseSchema:
        """Generate a UI component based on the user's request."""
        if request.dataset and request.dataset_name:
            try:
                decoded_bytes = base64.b64decode(request.dataset)
                data = decoded_bytes.decode("utf-8")
            except (base64.binascii.Error, UnicodeDecodeError) as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to decode or read dataset as string: {e}",
                )

        if data and self.component_descriptors is None:
            raise HTTPException(
                status_code=500, detail="There is no data and UI descriptor set."
            )

        try:
            component_response = await self.agent.generate_ui_component(
                question=request.prompt,
                data=data,
                component_descriptors=self.component_descriptors,
            )
            return component_response
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Error while generating component: {e}"
            )
