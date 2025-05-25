from vertexai import agent_engines
from custom_agent import CustomAgent
import vertexai
import os

vertexai.init(
    project=os.environ["PROJECT_ID"],
    location=os.environ["LOCATION"],
    staging_bucket=f"gs://{os.environ['BUCKET_NAME']}",
)

agent_engine = agent_engines.create(
    agent_engine=CustomAgent(),
    display_name="Custom agent sample",
    requirements=["google-cloud-aiplatform[agent-engines]>=1.94.0"],
    extra_packages=["custom_agent.py"],
)
