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

    def generate_content(self, message: str):
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=message,
        )
        return response.text

    def register_operations(self):
        return {
            "": [
                "generate_content",
                "create_session",
                "list_sessions",
                "delete_session",
            ],
        }


if __name__ == "__main__":
    agent = CustomAgent()
    agent.set_up()
    print(agent.list_sessions(user_id="test"))
