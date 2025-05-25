from vertexai import agent_engines
import os
from custom_agent import CustomAgent
import vertexai

vertexai.init(
    project=os.environ["PROJECT_ID"],
    location=os.environ["LOCATION"],
    staging_bucket=f"gs://{os.environ['BUCKET_NAME']}",
)

agent_engines.update(
    resource_name=os.environ["RESOURCE_ID"],
    agent_engine=CustomAgent(),
    requirements=[
        "google-cloud-aiplatform[adk,agent-engines]>=1.94.0",
        "google-genai>=1.16.1",
    ],
    display_name="Custom agent sample",
    extra_packages=["custom_agent.py"],
    env_vars={
        "PROJECT_ID": os.environ["PROJECT_ID"],
        "LOCATION": os.environ["LOCATION"],
    },
)
