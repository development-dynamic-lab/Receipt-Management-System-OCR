import os
from dotenv import load_dotenv   
from gemini import GeminiOCR

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_ocr = GeminiOCR(api_key = gemini_api_key)
image_file = "E:\\Python\\RyuKyuGlobal\\Project_OCR\\Images\\receipt_1.png"
gemini_ocr.AnalyzeReceipt(image_file = image_file)

