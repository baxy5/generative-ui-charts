import io
import json
import os
from typing import Annotated
import uuid
import boto3
from botocore.config import Config

from fastapi import Depends, HTTPException
from agents.iframe_component_agent import (
    IframeComponentAgent,
    IframeComponentRequestSchema,
    IframeComponentResponseSchema,
)


class IframeComponentService:
    """Service for interacting with the Agent and S3."""

    def __init__(self, agent: Annotated[IframeComponentAgent, Depends()]):
        self.agent = agent
        self.data = """{
  "companyProfile": {
    "name": "TechNova Solutions",
    "industry": "Enterprise Software",
    "founded": 2005,
    "headquarters": "San Francisco, CA",
    "mission": "Empowering businesses through innovative software solutions",
    "employees": {
      "total": 1250,
      "byDepartment": {
        "engineering": 450,
        "sales": 320,
        "marketing": 180,
        "customerSupport": 220,
        "administration": 80
      },
      "remotePercentage": 65
    },
    "leadership": [
      {
        "name": "Sarah Chen",
        "position": "CEO",
        "yearsInCompany": 15
      },
      {
        "name": "Michael Rodriguez",
        "position": "CTO",
        "yearsInCompany": 12
      },
      {
        "name": "Alicia Washington",
        "position": "CFO",
        "yearsInCompany": 8
      }
    ]
  },
  "financialOverview": {
    "currentValuation": "$850M",
    "lastFundingRound": {
      "series": "D",
      "amount": "$120M",
      "date": "2022-06-15",
      "leadInvestor": "Sequoia Capital"
    },
    "revenueStreams": {
      "subscriptions": 68,
      "professionalServices": 22,
      "partnerships": 10
    },
    "profitMargin": 28.5,
    "growthRate": {
      "fiveYear": 34.2,
      "threeYear": 42.7,
      "oneYear": 23.1
    }
  },
  "products": [
    {
      "name": "NovaSuite Enterprise",
      "category": "Enterprise Resource Planning",
      "launchYear": 2008,
      "annualRevenue": 1850000,
      "marketShare": 22.5,
      "customers": 450
    },
    {
      "name": "CloudSync Platform",
      "category": "Cloud Integration",
      "launchYear": 2012,
      "annualRevenue": 1250000,
      "marketShare": 18.3,
      "customers": 620
    },
    {
      "name": "SecureID Pro",
      "category": "Identity Management",
      "launchYear": 2016,
      "annualRevenue": 950000,
      "marketShare": 14.2,
      "customers": 780
    },
    {
      "name": "DataInsight Analytics",
      "category": "Business Intelligence",
      "launchYear": 2019,
      "annualRevenue": 650000,
      "marketShare": 8.7,
      "customers": 410
    }
  ],
  "customerMetrics": {
    "totalCustomers": 2260,
    "customerSegmentation": {
      "enterprise": 35,
      "midMarket": 45,
      "smallBusiness": 20
    },
    "acquisitionCost": 4200,
    "retentionRate": 92.5,
    "churnRate": 7.5,
    "nps": 72,
    "averageContractValue": 68000,
    "customerLifetimeValue": 420000
  },
  "marketPosition": {
    "globalRank": 12,
    "competitors": [
      {
        "name": "Enterprise Solutions Inc.",
        "marketShare": 28.5,
        "competitivePosition": "Leader"
      },
      {
        "name": "CloudSoft Technologies",
        "marketShare": 24.2,
        "competitivePosition": "Leader"
      },
      {
        "name": "TechNova Solutions",
        "marketShare": 18.3,
        "competitivePosition": "Challenger"
      },
      {
        "name": "Agile Systems",
        "marketShare": 12.5,
        "competitivePosition": "Challenger"
      },
      {
        "name": "NextGen Software",
        "marketShare": 9.8,
        "competitivePosition": "Niche Player"
      }
    ],
    "awards": [
      "Best Enterprise Software 2023 - Tech Excellence Awards",
      "Innovation Leader 2022 - Business Software Report",
      "Top Cloud Solution 2021 - Cloud Computing Magazine"
    ]
  },
  "geographicalPresence": {
    "regions": [
      {
        "name": "North America",
        "revenuePercentage": 45,
        "offices": ["San Francisco", "New York", "Toronto", "Chicago"]
      },
      {
        "name": "Europe",
        "revenuePercentage": 30,
        "offices": ["London", "Berlin", "Paris", "Amsterdam"]
      },
      {
        "name": "Asia Pacific",
        "revenuePercentage": 20,
        "offices": ["Singapore", "Tokyo", "Sydney", "Bangalore"]
      },
      {
        "name": "Latin America",
        "revenuePercentage": 5,
        "offices": ["Sao Paulo", "Mexico City"]
      }
    ],
    "expansionPlans": [
      {
        "region": "Middle East",
        "plannedOffices": ["Dubai", "Tel Aviv"],
        "targetDate": "2024-Q3",
        "projectedInvestment": 8500000
      },
      {
        "region": "Africa",
        "plannedOffices": ["Johannesburg", "Nairobi"],
        "targetDate": "2025-Q2",
        "projectedInvestment": 7200000
      }
    ]
  },
  "yearlyData": [
    {
      "year": 2005,
      "revenue": 1250000,
      "expenses": 850000,
      "profit": 400000,
      "profitMargin": 32.0,
      "employees": 45,
      "customers": 12,
      "marketShare": 1.2,
      "productCount": 1,
      "r_and_d_spending": 220000,
      "marketing_spending": 150000,
      "customer_acquisition_cost": 12500,
      "customer_retention_rate": 85.0
    },
    {
      "year": 2006,
      "revenue": 1450000,
      "expenses": 920000,
      "profit": 530000,
      "profitMargin": 36.5,
      "employees": 52,
      "customers": 18,
      "marketShare": 1.8,
      "productCount": 1,
      "r_and_d_spending": 250000,
      "marketing_spending": 180000,
      "customer_acquisition_cost": 11800,
      "customer_retention_rate": 86.5
    },
    {
      "year": 2007,
      "revenue": 1680000,
      "expenses": 1050000,
      "profit": 630000,
      "profitMargin": 37.5,
      "employees": 58,
      "customers": 26,
      "marketShare": 2.4,
      "productCount": 1,
      "r_and_d_spending": 290000,
      "marketing_spending": 210000,
      "customer_acquisition_cost": 10900,
      "customer_retention_rate": 87.2
    },
    {
      "year": 2008,
      "revenue": 1820000,
      "expenses": 1150000,
      "profit": 670000,
      "profitMargin": 36.8,
      "employees": 65,
      "customers": 42,
      "marketShare": 3.5,
      "productCount": 1,
      "r_and_d_spending": 320000,
      "marketing_spending": 230000,
      "customer_acquisition_cost": 10200,
      "customer_retention_rate": 88.0
    },
    {
      "year": 2009,
      "revenue": 1950000,
      "expenses": 1250000,
      "profit": 700000,
      "profitMargin": 35.9,
      "employees": 72,
      "customers": 68,
      "marketShare": 4.2,
      "productCount": 1,
      "r_and_d_spending": 350000,
      "marketing_spending": 260000,
      "customer_acquisition_cost": 9800,
      "customer_retention_rate": 89.1
    },
    {
      "year": 2010,
      "revenue": 2100000,
      "expenses": 1350000,
      "profit": 750000,
      "profitMargin": 35.7,
      "employees": 80,
      "customers": 95,
      "marketShare": 5.0,
      "productCount": 1,
      "r_and_d_spending": 380000,
      "marketing_spending": 290000,
      "customer_acquisition_cost": 9500,
      "customer_retention_rate": 89.8
    },
    {
      "year": 2011,
      "revenue": 2250000,
      "expenses": 1450000,
      "profit": 800000,
      "profitMargin": 35.5,
      "employees": 88,
      "customers": 125,
      "marketShare": 5.6,
      "productCount": 1,
      "r_and_d_spending": 410000,
      "marketing_spending": 320000,
      "customer_acquisition_cost": 9200,
      "customer_retention_rate": 90.2
    },
    {
      "year": 2012,
      "revenue": 2400000,
      "expenses": 1550000,
      "profit": 850000,
      "profitMargin": 35.4,
      "employees": 95,
      "customers": 168,
      "marketShare": 6.3,
      "productCount": 2,
      "r_and_d_spending": 450000,
      "marketing_spending": 350000,
      "customer_acquisition_cost": 8900,
      "customer_retention_rate": 90.5
    },
    {
      "year": 2013,
      "revenue": 2550000,
      "expenses": 1650000,
      "profit": 900000,
      "profitMargin": 35.2,
      "employees": 102,
      "customers": 210,
      "marketShare": 6.8,
      "productCount": 2,
      "r_and_d_spending": 480000,
      "marketing_spending": 380000,
      "customer_acquisition_cost": 8600,
      "customer_retention_rate": 90.8
    },
    {
      "year": 2014,
      "revenue": 2700000,
      "expenses": 1750000,
      "profit": 950000,
      "profitMargin": 35.1,
      "employees": 110,
      "customers": 256,
      "marketShare": 7.4,
      "productCount": 2,
      "r_and_d_spending": 510000,
      "marketing_spending": 410000,
      "customer_acquisition_cost": 8300,
      "customer_retention_rate": 91.0
    },
    {
      "year": 2015,
      "revenue": 2850000,
      "expenses": 1850000,
      "profit": 1000000,
      "profitMargin": 35.0,
      "employees": 118,
      "customers": 312,
      "marketShare": 8.1,
      "productCount": 2,
      "r_and_d_spending": 540000,
      "marketing_spending": 440000,
      "customer_acquisition_cost": 8000,
      "customer_retention_rate": 91.3
    },
    {
      "year": 2016,
      "revenue": 3000000,
      "expenses": 1950000,
      "profit": 1050000,
      "profitMargin": 35.0,
      "employees": 125,
      "customers": 380,
      "marketShare": 8.9,
      "productCount": 3,
      "r_and_d_spending": 580000,
      "marketing_spending": 480000,
      "customer_acquisition_cost": 7700,
      "customer_retention_rate": 91.6
    },
    {
      "year": 2017,
      "revenue": 3150000,
      "expenses": 2050000,
      "profit": 1100000,
      "profitMargin": 34.9,
      "employees": 132,
      "customers": 452,
      "marketShare": 9.6,
      "productCount": 3,
      "r_and_d_spending": 620000,
      "marketing_spending": 520000,
      "customer_acquisition_cost": 7400,
      "customer_retention_rate": 91.8
    },
    {
      "year": 2018,
      "revenue": 3300000,
      "expenses": 2150000,
      "profit": 1150000,
      "profitMargin": 34.8,
      "employees": 140,
      "customers": 528,
      "marketShare": 10.3,
      "productCount": 3,
      "r_and_d_spending": 660000,
      "marketing_spending": 560000,
      "customer_acquisition_cost": 7100,
      "customer_retention_rate": 92.0
    },
    {
      "year": 2019,
      "revenue": 3450000,
      "expenses": 2250000,
      "profit": 1200000,
      "profitMargin": 34.7,
      "employees": 148,
      "customers": 612,
      "marketShare": 11.1,
      "productCount": 4,
      "r_and_d_spending": 710000,
      "marketing_spending": 610000,
      "customer_acquisition_cost": 6800,
      "customer_retention_rate": 92.1
    },
    {
      "year": 2020,
      "revenue": 3600000,
      "expenses": 2350000,
      "profit": 1250000,
      "profitMargin": 34.7,
      "employees": 155,
      "customers": 725,
      "marketShare": 12.5,
      "productCount": 4,
      "r_and_d_spending": 760000,
      "marketing_spending": 660000,
      "customer_acquisition_cost": 6500,
      "customer_retention_rate": 92.2
    },
    {
      "year": 2021,
      "revenue": 3750000,
      "expenses": 2450000,
      "profit": 1300000,
      "profitMargin": 34.6,
      "employees": 162,
      "customers": 845,
      "marketShare": 13.8,
      "productCount": 4,
      "r_and_d_spending": 810000,
      "marketing_spending": 710000,
      "customer_acquisition_cost": 6200,
      "customer_retention_rate": 92.3
    },
    {
      "year": 2022,
      "revenue": 3900000,
      "expenses": 2550000,
      "profit": 1350000,
      "profitMargin": 34.6,
      "employees": 170,
      "customers": 980,
      "marketShare": 15.2,
      "productCount": 4,
      "r_and_d_spending": 860000,
      "marketing_spending": 760000,
      "customer_acquisition_cost": 5900,
      "customer_retention_rate": 92.4
    },
    {
      "year": 2023,
      "revenue": 4050000,
      "expenses": 2650000,
      "profit": 1400000,
      "profitMargin": 34.5,
      "employees": 178,
      "customers": 1120,
      "marketShare": 16.4,
      "productCount": 4,
      "r_and_d_spending": 910000,
      "marketing_spending": 810000,
      "customer_acquisition_cost": 5600,
      "customer_retention_rate": 92.4
    },
    {
      "year": 2024,
      "revenue": 4200000,
      "expenses": 2750000,
      "profit": 1450000,
      "profitMargin": 34.5,
      "employees": 185,
      "customers": 1265,
      "marketShare": 17.6,
      "productCount": 4,
      "r_and_d_spending": 960000,
      "marketing_spending": 860000,
      "customer_acquisition_cost": 5300,
      "customer_retention_rate": 92.5
    },
    {
      "year": 2025,
      "revenue": 4350000,
      "expenses": 2850000,
      "profit": 1500000,
      "profitMargin": 34.4,
      "employees": 192,
      "customers": 1420,
      "marketShare": 18.3,
      "productCount": 4,
      "r_and_d_spending": 1010000,
      "marketing_spending": 910000,
      "customer_acquisition_cost": 5000,
      "customer_retention_rate": 92.5
    }
  ],
  "sustainabilityMetrics": {
    "carbonFootprint": {
      "2020": 12500,
      "2021": 11200,
      "2022": 9800,
      "2023": 8400,
      "2024": 7200,
      "2025Target": 6000
    },
    "renewableEnergyUsage": {
      "2020": 35,
      "2021": 42,
      "2022": 58,
      "2023": 72,
      "2024": 85,
      "2025Target": 100
    },
    "wasteReduction": {
      "2020": 15,
      "2021": 22,
      "2022": 28,
      "2023": 35,
      "2024": 45,
      "2025Target": 60
    },
    "sustainabilityInitiatives": [
      "Paperless Office Program",
      "Remote Work Carbon Reduction",
      "Sustainable Data Center Operations",
      "Green Supply Chain Management"
    ]
  },
  "researchAndDevelopment": {
    "currentProjects": [
      {
        "name": "AI-Powered Business Analytics",
        "startDate": "2023-03",
        "completionTarget": "2024-Q2",
        "budget": 1250000,
        "teamSize": 18,
        "status": "In Progress"
      },
      {
        "name": "Blockchain Integration Platform",
        "startDate": "2023-08",
        "completionTarget": "2024-Q3",
        "budget": 950000,
        "teamSize": 12,
        "status": "In Progress"
      },
      {
        "name": "Low-Code Enterprise Solutions",
        "startDate": "2023-11",
        "completionTarget": "2024-Q4",
        "budget": 820000,
        "teamSize": 10,
        "status": "Planning"
      }
    ],
    "patents": {
      "filed": 48,
      "granted": 32,
      "pending": 16
    },
    "partnerships": [
      {
        "partner": "Stanford University",
        "focus": "AI Research",
        "startYear": 2021
      },
      {
        "partner": "MIT",
        "focus": "Data Science",
        "startYear": 2022
      },
      {
        "partner": "ETH Zurich",
        "focus": "Cybersecurity",
        "startYear": 2023
      }
    ]
  }
}
"""
        self.data_new = """{
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

    def create_separate_files(self, agent_response):
        """Build separate codes."""

        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{agent_response.page_title}</title>
            <link rel="stylesheet" href="./styles.css">
        </head>
        <body>
            <div class="component-container">
                {agent_response.html}
            </div>
            
            <script src="./app.js"></script>
            <script>
                // Initialize component when DOM is loaded
                document.addEventListener('DOMContentLoaded', function() {{
                    if (window.initializeComponent) {{
                        window.initializeComponent('1');
                    }}
                }});
            </script>
        </body>
        </html>
        """

        css_content = agent_response.css

        js_content = agent_response.js

        return {"html": html_content, "css": css_content, "javascript": js_content}

    async def upload_to_storage(self, files) -> str:
        """Upload files to Cloudflare R2 Object Storage and return the hosted URL."""

        # Cloudflare R2 Config
        account_id = os.getenv("CLOUDFLARE_ACCOUNT_ID")
        access_key_id = os.getenv("CLOUDFLARE_R2_ACCESS_KEY_ID")
        secret_access_key = os.getenv("CLOUDFLARE_R2_SECRET_ACCESS_KEY")
        bucket_name = os.getenv("CLOUDFLARE_R2_BUCKET_NAME")

        if not all([account_id, access_key_id, secret_access_key]):
            raise ValueError("Missing required Cloudflare R2 environment variables")

        # Configure boto3 client for Cloudflare R2
        r2_client = boto3.client(
            "s3",
            endpoint_url=f"https://{account_id}.r2.cloudflarestorage.com",
            aws_access_key_id=access_key_id,
            aws_secret_access_key=secret_access_key,
            config=Config(signature_version="s3v4"),
            region_name="auto",
        )

        # Create unique uuid for this app
        folder_key = f"{str(uuid.uuid4()).replace('-', '')[:12]}"

        files_to_upload = [
            ("index.html", files["html"], "text/html"),
            ("styles.css", files["css"], "text/css"),
            ("app.js", files["javascript"], "application/javascript"),
        ]

        try:
            for filename, content, content_type in files_to_upload:
                file_key = f"{folder_key}/{filename}"

                r2_client.put_object(
                    Bucket=bucket_name,
                    Key=file_key,
                    Body=content,
                    ContentType=content_type,
                )

            return f"https://pub-b348006f0b2142f7a105983d74576412.r2.dev/{folder_key}/index.html"

        except Exception as e:
            raise Exception(f"Failed to upload files to Cloudflare R2: {str(e)}")

    async def generate_iframe_component(
        self, request: IframeComponentRequestSchema
    ) -> IframeComponentResponseSchema:
        try:
            # Generate page_title, HTML, CSS and JS code.
            agent_response = await self.agent.generate_iframe_components(
                question=request.question,
                data=self.data_new,
                ui_descriptor=self.ui_descriptors,
                css=self.css_descriptors,
            )

            # TODO: Do I need this?
            # component_id = str(uuid.uuid4()).replace('-', '')[:12]

            # Build separate HTML, CSS and Javascript files.
            files = self.create_separate_files(agent_response)

            # Upload to S3 and get url
            hosted_url = await self.upload_to_storage(files)

            return IframeComponentResponseSchema(id="1", url=hosted_url)
        except Exception as e:
            raise HTTPException(
                status_code=500, detail=f"Failed to generate URL for Iframe: {e}"
            )
