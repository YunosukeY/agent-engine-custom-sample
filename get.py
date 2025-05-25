from vertexai import agent_engines
import os

agent_engine = agent_engines.get(os.environ["RESOURCE_ID"])
print(agent_engine.generate_content(message="Why is the sky blue?"))
