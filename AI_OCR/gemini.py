##Imports
from google import genai
from google.genai import types
from AI_OCR.modules.system_instruction import system_prompt
from AI_OCR.modules.extract_text import ExtractText

class GeminiOCR:
    def __init__(self, api_key=None):
        # Initialize GeminiOCR with API key
        if api_key is None:
            raise ValueError("Please provide an api key!")
        
        self.apiKey = api_key
        # Create a GenAI client using the API key
        self.client = genai.Client(api_key=self.apiKey)
        

    def analyze_receipt(self, image_file):
        try:
            client = self.client
            
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
                            text =  system_prompt
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
                # print(chunk.text, end="")  # make a logger instead
                
            ##if uploaded image is not a japanese receipt
            if full_response.strip() == '[]':
                return 'wrong_image'
            
            # return full_response
            extractText = ExtractText(text = full_response)
            final_response = extractText.do_extraction()
            return final_response
            
            
            
        except Exception as e:
            return "Oops! Something wrong!!"
        


