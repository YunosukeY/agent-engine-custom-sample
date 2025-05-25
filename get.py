from vertexai import agent_engines
import os

agent_engine = agent_engines.get(os.environ["RESOURCE_ID"])
print(
    agent_engine.list_messages(
        user_id="test",
        session_id="4465438327549460480",
    )
)
