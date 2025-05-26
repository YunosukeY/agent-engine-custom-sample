from typing import TypedDict
from google.adk.events import Event
from google.genai.types import UserContent, ModelContent
from google import genai
from google.adk.sessions import VertexAiSessionService
import os

class Message(TypedDict):
    id: str
    author: str
    content: str
    timestamp: float


class CustomAgent:
    def __init__(self, project_id: str, location: str, model: str):
        self.project_id = project_id
        self.location = location
        self.model = model

    def set_up(self):
        self.client = genai.Client(
            vertexai=True,
            project=self.project_id,
            location=self.location,
        )
        self.session_service = VertexAiSessionService(
            self.project_id,
            self.location,
        )
        self.app_name = os.environ["GOOGLE_CLOUD_AGENT_ENGINE_ID"]

    def create_session(self, user_id: str):
        session = self.session_service.create_session(
            app_name=self.app_name,
            user_id=user_id,
        )
        return session.id

    def list_sessions(self, user_id: str):
        response = self.session_service.list_sessions(
            app_name=self.app_name,
            user_id=user_id,
        )
        return [session.id for session in response.sessions]

    def delete_session(self, user_id: str, session_id: str):
        self.session_service.delete_session(
            app_name=self.app_name,
            user_id=user_id,
            session_id=session_id,
        )

    def send_message(self, user_id: str, session_id: str, message: str):
        session = self.session_service.get_session(
            app_name=self.app_name,
            user_id=user_id,
            session_id=session_id,
        )
        history = [event.content for event in session.events if event.content is not None]

        user_content = UserContent(message)
        response = self.client.models.generate_content(
            model=self.model,
            contents=history + [user_content],
        )

        user_event = Event(
            invocation_id=response.response_id,
            author="user",
            content=user_content,
        )
        self.session_service.append_event(
            session=session,
            event=user_event,
        )

        agent_event = Event(
            invocation_id=response.response_id,
            author="agent",
            content=ModelContent(response.text),
        )
        self.session_service.append_event(
            session=session,
            event=agent_event,
        )

        return response.text

    def send_message_stream(self, user_id: str, session_id: str, message: str):
        session = self.session_service.get_session(
            app_name=self.app_name,
            user_id=user_id,
            session_id=session_id,
        )
        history = [event.content for event in session.events if event.content is not None]

        user_content = UserContent(message)
        response_text = ""
        for chunk in self.client.models.generate_content_stream(
            model=self.model,
            contents=history + [user_content],
        ):
            response_id = chunk.response_id
            response_text += chunk.text
            yield chunk.text

        user_event = Event(
            invocation_id=response_id,
            author="user",
            content=user_content,
        )
        self.session_service.append_event(
            session=session,
            event=user_event,
        )

        agent_event = Event(
            invocation_id=response_id,
            author="agent",
            content=ModelContent(response_text),
        )
        self.session_service.append_event(
            session=session,
            event=agent_event,
        )

    def list_messages(self, user_id: str, session_id: str):
        response = self.session_service.list_events(
            app_name=self.app_name,
            user_id=user_id,
            session_id=session_id,
        )
        return [
            Message(
                id=event.id,
                author=event.author,
                content=event.content.parts[0].text,
                timestamp=event.timestamp,
            )
            for event in response.events
        ]

    def register_operations(self):
        return {
            "": [
                "create_session",
                "list_sessions",
                "delete_session",
                "send_message",
                "list_messages",
            ],
            "stream": ["send_message_stream"],
        }
