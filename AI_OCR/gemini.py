##Imports
from google import genai
from google.genai import types

class GeminiOCR:
    def __init__(self, api_key=None):
        # Initialize GeminiOCR with API key
        if api_key is None:
            raise ValueError("Please provide an api key!")
        
        self.apiKey = api_key

    def AnalyzeReceipt(self, image_file):
        # Create a GenAI client using the API key
        client = genai.Client(api_key=self.apiKey)

        # Upload the image file
        files = [
            client.files.upload(file=image_file),
        ]

        # Set the model and request contents
        model = "gemini-2.0-flash"
        contents = [
            types.Content(
                role="user",
                parts=[
                    types.Part.from_uri(
                        file_uri=files[0].uri,
                        mime_type=files[0].mime_type,
                    ),
                    types.Part.from_text(
                        text="Can you please analyze the Japanese receipt and help me extract important fields and nitty gritty details. Thank you!"
                    ),
                ],
            ),
        ]

        # Set response configuration
        generate_content_config = types.GenerateContentConfig(
            response_mime_type="text/plain",
        )

        # Stream the model's response
        full_response = ""
        for chunk in client.models.generate_content_stream(
            model=model,
            contents=contents,
            config=generate_content_config,
        ):
            full_response += chunk.text
            print(chunk.text, end="")  # Optional: print as it streams

        return full_response


