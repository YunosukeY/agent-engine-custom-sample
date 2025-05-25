from vertexai import agent_engines
import os

agent_engine = agent_engines.get(os.environ["RESOURCE_ID"])
for chunk in agent_engine.send_message_stream(
    user_id="test",
    session_id="4465438327549460480",
    message="Hello, how are you?",
):
    print(chunk)
