from vertexai import agent_engines
import os

agent_engine = agent_engines.get(os.environ["RESOURCE_ID"])
print(agent_engine.list_sessions(user_id="test"))
