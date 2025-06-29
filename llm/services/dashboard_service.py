import json
import os
from typing import Annotated, List
from fastapi import Depends, HTTPException
from agents.dashboard_agent import (
    AgentState,
    DashboardAgent,
    DashboardRequestSchema,
    DashboardResponseSchema,
)
from langchain_core.runnables.config import RunnableConfig
from core.store_to_r2 import Files, R2ObjectStorage


class DashboardService:
    """Service for interacing with Dashboard Agent."""

    def __init__(
        self,
        agent: Annotated[DashboardAgent, Depends()],
        r2: Annotated[
            R2ObjectStorage,
            Depends(
                lambda: R2ObjectStorage(
                    "https://pub-b348006f0b2142f7a105983d74576412.r2.dev"
                )
            ),
        ],
    ) -> None:
        self.agent = agent
        self.r2 = r2
        self.data = """{
            "company": {
                "name": "QuantumLeap Tech",
                "foundedYear": 2015,
                "headquarters": "San Francisco, CA",
                "industry": "Artificial Intelligence",
                "description": "QuantumLeap Tech is a pioneer in developing cutting-edge AI-driven solutions for businesses, focusing on machine learning, natural language processing, and computer vision to solve complex real-world problems.",
                "missionStatement": "To empower humanity with intelligent technology, making life and work more efficient, creative, and sustainable.",
                "financials": {
                "2023": {
                    "revenue": 50000000,
                    "netIncome": 12000000,
                    "EBITDA": 18000000,
                    "currency": "USD"
                },
                "2022": {
                    "revenue": 35000000,
                    "netIncome": 8000000,
                    "EBITDA": 11000000,
                    "currency": "USD"
                }
                },
                "kpis": {
                "customerSatisfaction": "95%",
                "customerChurnRate": "5%",
                "employeeTurnoverRate": "10%",
                "netPromoterScore": 8.5,
                "marketShare": "15%"
                },
                "products": [
                {
                    "productId": "QL-NLP-001",
                    "productName": "Nexus AI",
                    "description": "An advanced natural language processing platform that offers sentiment analysis, text summarization, and language translation services through a powerful API.",
                    "launchYear": 2018,
                    "annualRevenue": 20000000,
                    "kpis": {
                    "activeUsers": 150000,
                    "apiCallsPerMonth": 100000000,
                    "customerAcquisitionCost": 50,
                    "customerLifetimeValue": 500,
                    "userAdoptionRate": "60%"
                    }
                },
                {
                    "productId": "QL-CV-002",
                    "productName": "Visionary Suite",
                    "description": "A computer vision software suite for image recognition, object detection, and video analysis, tailored for retail and security industries.",
                    "launchYear": 2020,
                    "annualRevenue": 15000000,
                    "kpis": {
                    "activeUsers": 5000,
                    "apiCallsPerMonth": 20000000,
                    "customerAcquisitionCost": 200,
                    "customerLifetimeValue": 2500,
                    "userAdoptionRate": "45%"
                    }
                },
                {
                    "productId": "QL-ML-003",
                    "productName": "Synapse ML",
                    "description": "A machine learning platform that enables developers to build, train, and deploy custom ML models with ease.",
                    "launchYear": 2022,
                    "annualRevenue": 15000000,
                    "kpis": {
                    "activeUsers": 10000,
                    "modelsDeployed": 5000,
                    "customerAcquisitionCost": 150,
                    "customerLifetimeValue": 1800,
                    "userAdoptionRate": "55%"
                    }
                }
                ],
                "leadership": [
                {
                    "employeeId": "QL-00001",
                    "name": "Dr. Evelyn Reed",
                    "age": 45,
                    "role": "Chief Executive Officer",
                    "experienceYears": 20,
                    "specialization": ["Business Strategy", "AI Ethics"],
                    "contact": {
                    "email": "evelyn.reed@quantumleap.tech",
                    "phone": "123-456-7890"
                    },
                    "performance": {
                    "lastReviewScore": 4.9,
                    "strategicGoalsMet": "98%"
                    },
                    "bio": "Dr. Reed co-founded QuantumLeap with a vision to revolutionize industries with AI. With a Ph.D. in Computer Science, she has led the company to its current success."
                },
                {
                    "employeeId": "QL-00002",
                    "name": "Ben Carter",
                    "age": 42,
                    "role": "Chief Technology Officer",
                    "experienceYears": 18,
                    "specialization": ["Machine Learning", "System Architecture"],
                    "contact": {
                    "email": "ben.carter@quantumleap.tech",
                    "phone": "123-456-7891"
                    },
                    "performance": {
                    "lastReviewScore": 4.8,
                    "projectsOverseen": 50
                    },
                    "bio": "Ben is the architect behind QuantumLeap's robust and scalable technology platforms. He holds multiple patents in machine learning algorithms."
                }
                ],
                "teams": [
                {
                    "teamId": "TEAM-NLP-01",
                    "teamName": "Nexus AI Development",
                    "teamGoal": "Enhance the capabilities of the Nexus AI platform and expand its market reach.",
                    "teamLead": {
                    "employeeId": "QL-00101",
                    "name": "Aisha Khan",
                    "age": 35,
                    "role": "Lead NLP Engineer",
                    "experienceYears": 12,
                    "specialization": ["Natural Language Processing", "Deep Learning"],
                    "contact": {
                        "email": "aisha.khan@quantumleap.tech",
                        "phone": "234-567-8901"
                    },
                    "performance": {
                        "lastReviewScore": 4.7,
                        "projectsCompleted": 15
                    }
                    },
                    "members": [
                    {
                        "employeeId": "QL-00102",
                        "name": "Carlos Gomez",
                        "age": 30,
                        "role": "Senior Software Engineer",
                        "experienceYears": 8,
                        "specialization": ["Python", "API Development"],
                        "contact": {
                        "email": "carlos.gomez@quantumleap.tech"
                        },
                        "performance": {
                        "lastReviewScore": 4.5,
                        "tasksCompletedOnTime": "95%"
                        }
                    },
                    {
                        "employeeId": "QL-00103",
                        "name": "Mei Lin",
                        "age": 28,
                        "role": "Data Scientist",
                        "experienceYears": 5,
                        "specialization": ["Sentiment Analysis", "Statistical Modeling"],
                        "contact": {
                        "email": "mei.lin@quantumleap.tech"
                        },
                        "performance": {
                        "lastReviewScore": 4.6,
                        "modelAccuracyImprovedBy": "10%"
                        }
                    }
                    ]
                },
                {
                    "teamId": "TEAM-CV-01",
                    "teamName": "Visionary Suite Engineering",
                    "teamGoal": "Develop new features for the Visionary Suite and ensure its reliability and performance.",
                    "teamLead": {
                    "employeeId": "QL-00201",
                    "name": "David Chen",
                    "age": 38,
                    "role": "Lead Computer Vision Engineer",
                    "experienceYears": 15,
                    "specialization": ["Computer Vision", "C++"],
                    "contact": {
                        "email": "david.chen@quantumleap.tech",
                        "phone": "345-678-9012"
                    },
                    "performance": {
                        "lastReviewScore": 4.8,
                        "projectsCompleted": 20
                    }
                    },
                    "members": [
                    {
                        "employeeId": "QL-00202",
                        "name": "Sophia Rodriguez",
                        "age": 32,
                        "role": "Software Engineer",
                        "experienceYears": 7,
                        "specialization": ["Image Processing", "GPU Programming"],
                        "contact": {
                        "email": "sophia.rodriguez@quantumleap.tech"
                        },
                        "performance": {
                        "lastReviewScore": 4.4,
                        "bugsFixed": 150
                        }
                    },
                    {
                        "employeeId": "QL-00203",
                        "name": "Tom Anderson",
                        "age": 29,
                        "role": "QA Engineer",
                        "experienceYears": 6,
                        "specialization": ["Automated Testing", "CI/CD"],
                        "contact": {
                        "email": "tom.anderson@quantumleap.tech"
                        },
                        "performance": {
                        "lastReviewScore": 4.5,
                        "testCoverage": "98%"
                        }
                    }
                    ]
                }
                ]
            }
            }
            """
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            file_path = os.path.join(
                current_dir, "..", "public-mock-data", "component_library.json"
            )
            with open(file_path, "r") as f:
                component_data = json.load(f)
            self.ui_descriptors = json.dumps(component_data)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Failed to load or parse component_library.json: {e}")
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            css_file_path = os.path.join(
                current_dir, "..", "public-mock-data", "styles.css"
            )
            with open(css_file_path, "r") as f:
                self.css_descriptors = f.read()
        except (FileNotFoundError, UnicodeDecodeError) as e:
            raise RuntimeError(f"Failed to load or parse globals.css: {e}")

    async def generate_dashboard(self, request: DashboardRequestSchema):
        try:
            config = RunnableConfig(configurable={"thread_id": "1"})

            if request.phase == "generate_layouts":
                initial_state: AgentState = {
                    "question": request.question,
                    "data": self.data,
                    "phase": "generate_layouts",
                    "selected_layout_id": None,
                    "css_descriptor": None,
                    "ui_descriptor": None,
                }
                result = await self.agent.graph.ainvoke(initial_state, config=config)
                response_layouts = result["result"].layouts

                hosted_urls = []
                for layout in response_layouts:
                    files_obj = {
                        "page_title": layout.page_title,
                        "html": layout.html,
                        "css": layout.css,
                        "js": layout.js,
                    }
                    hosted_url = await self.r2.upload_to_storage(files_obj)
                    hosted_urls.append(hosted_url)

                return DashboardResponseSchema(
                    url=hosted_urls, layouts=response_layouts
                )
            else:
                if not request.selected_layout_id:
                    raise HTTPException(
                        status_code=400,
                        detail="selected_layout_id required for finalize phase",
                    )

                # load descriptors
                initial_state: AgentState = {
                    "question": request.question,
                    "data": self.data,
                    "phase": "finalize_dashboard",
                    "selected_layout_id": request.selected_layout_id,
                    "css_descriptor": None,
                    "ui_descriptor": None,
                }

                result = await self.agent.graph.ainvoke(initial_state, config=config)
                response_layouts = result["result"].layouts

                hosted_urls = []
                for layout in response_layouts:
                    files_obj = {
                        "page_title": layout.page_title,
                        "html": layout.html,
                        "css": layout.css,
                        "js": layout.js,
                    }
                    hosted_url = await self.r2.upload_to_storage(files_obj)
                    hosted_urls.append(hosted_url)

                return DashboardResponseSchema(
                    url=hosted_urls, layouts=response_layouts
                )
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Service -> Dashboard generation failed: {e}"
            )
