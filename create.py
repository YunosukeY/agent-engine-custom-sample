from vertexai import agent_engines
import os
from custom_agent import CustomAgent
import vertexai

PROJECT_ID = os.environ["PROJECT_ID"]
LOCATION = os.environ["LOCATION"]
BUCKET_NAME = os.environ["BUCKET_NAME"]
RESOURCE_ID = os.environ["RESOURCE_ID"]

vertexai.init(
    project=PROJECT_ID,
    location=LOCATION,
    staging_bucket=f"gs://{BUCKET_NAME}",
)

agent_engines.create(
    agent_engine=CustomAgent(
        project_id=PROJECT_ID,
        location=LOCATION,
        model="gemini-2.5-flash-preview-05-20",
    ),
    requirements=[
        "google-cloud-aiplatform[adk,agent-engines]>=1.94.0",
        "google-genai>=1.16.1",
    ],
    display_name="Custom agent sample",
    extra_packages=["custom_agent.py"],
)
