from typing import Optional, Union
from fastapi import FastAPI
from pydantic import BaseModel, Field
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv

from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, HumanMessage

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("Api key is not set for Openai.")


class ResponseSchema(BaseModel):
    name: Optional[str] = Field(default=None, description="Name of the component.")
    component: Optional[str] = Field(default=None, description="Component code.")
    rechartComponents: Optional[list[str]] = Field(
        default=None, description="List of rechart components used in the component."
    )


model = init_chat_model("gpt-4o-mini", model_provider="openai")
model_with_structured_output = model.with_structured_output(ResponseSchema)
messages = [
    SystemMessage(
        "You are a helpful assistant that generates a react component using Recharts library based on the user's request."
    ),
    # SystemMessage("The component must not contain import statements in the beginning. For example React import, Rechart component imports."),
    HumanMessage(
        content="""I want a Line chart from this data: const data = [
    { year: '2023', amount: 34000 },
    { year: '2024', amount: 19000 },
    { year: '2025', amount: 20000 },
    ];"""
    ),
]


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# TODO: Prompt the ai to generate the component without the initial imports

TEST_RESPONSE = """
    const data = [
    { year: '2023', amount: 34000 },
    { year: '2024', amount: 19000 },
    { year: '2025', amount: 20000 },
    ];

    function FinanceBarChart() {
    return (
        <ResponsiveContainer width="100%" height={300}>
        <BarChart data={data} margin={{ top: 20, right: 30, left: 10, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="year" />
            <YAxis tickFormatter={(value) => `${value} Ft`} />
            <Tooltip formatter={(value) => `${value} Ft`} />
            <Bar dataKey="amount" fill="#8884d8" radius={[4, 4, 0, 0]} />
        </BarChart>
        </ResponsiveContainer>
    );
    }

    export default FinanceBarChart;
"""

TEST_RESPONSE_FULL = """
import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
const data = [{
  year: '2023',
  amount: 34000
}, {
  year: '2024',
  amount: 19000
}, {
  year: '2025',
  amount: 20000
}];
const LineChartComponent = () => {
  return /*#__PURE__*/React.createElement(ResponsiveContainer, {
    width: "100%",
    height: 400
  }, /*#__PURE__*/React.createElement(LineChart, {
    data: data
  }, /*#__PURE__*/React.createElement(CartesianGrid, {
    strokeDasharray: "3 3"
  }), /*#__PURE__*/React.createElement(XAxis, {
    dataKey: "year"
  }), /*#__PURE__*/React.createElement(YAxis, null), /*#__PURE__*/React.createElement(Tooltip, null), /*#__PURE__*/React.createElement(Legend, null), /*#__PURE__*/React.createElement(Line, {
    type: "monotone",
    dataKey: "amount",
    stroke: "#8884d8",
    activeDot: {
      r: 8
    }
  })));
};
export default LineChartComponent;
"""


@app.get("/")
def hello():
    return {"message": "hello"}


@app.get("/generative-ui")
def generative_ui():
    response = model_with_structured_output.invoke(messages)
    return {"message": response}
