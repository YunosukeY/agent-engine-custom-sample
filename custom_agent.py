class CustomAgent:
    def __init__(self):
        pass

    def set_up(self):
        from google import genai
        import os

        self.client = genai.Client(
            vertexai=True,
            project=os.environ["PROJECT_ID"],
            location=os.environ["LOCATION"],
        )

    def generate_content(self, message: str):
        response = self.client.models.generate_content(
            model="gemini-2.0-flash-001",
            contents=message,
        )
        return response.text

    def register_operations(self):
        return {
            "": ["generate_content"],
        }
