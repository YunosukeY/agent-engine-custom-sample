from vertexai import agent_engines
import os


RESOURCE_ID = os.environ["RESOURCE_ID"]

agent_engine = agent_engines.get(RESOURCE_ID)
user_id = "test"

session_id = agent_engine.create_session(user_id=user_id)
print(agent_engine.list_sessions(user_id=user_id))

print(agent_engine.send_message(user_id=user_id, session_id=session_id, message="私の名前は山田太郎です。"))
for chunk in agent_engine.send_message_stream(user_id=user_id, session_id=session_id, message="私の名前はなんでしょう。"):
    print(chunk)

print(agent_engine.list_messages(user_id=user_id, session_id=session_id))

agent_engine.delete_session(user_id=user_id, session_id=session_id)
print(agent_engine.list_sessions(user_id=user_id))
