from typing import TypedDict


class Message(TypedDict):
    id: str
    author: str
    content: str
    timestamp: float


class CustomAgent:
    def set_up(self):
        from google import genai
        from google.adk.sessions import VertexAiSessionService
        import os

        self.client = genai.Client(
            vertexai=True,
            project=os.environ["PROJECT_ID"],
            location=os.environ["LOCATION"],
        )
        self.session_service = VertexAiSessionService(
            os.environ["PROJECT_ID"],
            os.environ["LOCATION"],
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
        from google.adk.events import Event
        from google.genai.types import UserContent, ModelContent

        session = self.session_service.get_session(
            app_name=self.app_name,
            user_id=user_id,
            session_id=session_id,
        )

        response = self.client.models.generate_content(
            model="gemini-2.5-flash-preview-05-20",
            contents=message,
        )

        user_event = Event(
            invocation_id=response.response_id,
            author="user",
            content=UserContent(message),
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
        from google.adk.events import Event
        from google.genai.types import UserContent, ModelContent

        session = self.session_service.get_session(
            app_name=self.app_name,
            user_id=user_id,
            session_id=session_id,
        )

        response_text = ""
        for chunk in self.client.models.generate_content_stream(
            model="gemini-2.5-flash-preview-05-20",
            contents=message,
        ):
            response_id = chunk.response_id
            response_text += chunk.text
            yield chunk.text

        user_event = Event(
            invocation_id=response_id,
            author="user",
            content=UserContent(message),
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
