import json
from typing import Annotated, Any, Optional
from fastapi import Depends
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from core.common import get_gpt_client
from langchain_core.messages import HumanMessage, SystemMessage


class RechartRequestSchema(BaseModel):
    prompt: str


class RechartResponseSchema(BaseModel):
    name: Optional[str] = Field(default=None, description="Name of the component.")
    component: Optional[str] = Field(default=None, description="Component code.")
    rechartComponents: Optional[list[str]] = Field(
        default=None, description="List of rechart components used in the component."
    )


class RechartAgent:
    """Agent for Rechart graph generation."""

    def __init__(self, client: Annotated[ChatOpenAI, Depends(get_gpt_client)]):
        self.client = client

    async def generate_ui_rechart(
        self, request: RechartRequestSchema, data: Any | dict
    ) -> RechartResponseSchema:
        try:
            user_prompt = request.prompt
            model = self.client.with_structured_output(RechartResponseSchema)
            data_summary = json.dumps(data)
            messages = [
                SystemMessage(
                    f"""You are a helpful assistant that generates a react component using Recharts library based on the medical data and user requests.
            
            Medical data:
            {data_summary}
            
            1. Use the Recharts library components
            2. Use the ResponsiveContainer component to ensure the chart is responsive
            3. The "data" variable must be defined in the beginning of the component
            4. Create complete React components that visualize the data according to user requests
            5. The component must end with the "export default [componentName]" statement
            6. Return clean, well-structured React code
            
            This dataset contains multiple medical test results over time with various measurements.
            """
                ),
                HumanMessage(content=f"""Using the medical data, {user_prompt}"""),
            ]

            response = await model.ainvoke(messages)

            return response
        except Exception as e:
            print(f"Error while generating Rechart component: {e}")
            return RechartResponseSchema(
                name="Error",
                component="Failed to generate Rechart component.",
                rechartComponents=[],
            )
