import os
from dotenv import load_dotenv   
from gemini import GeminiOCR

load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")
gemini_ocr = GeminiOCR(api_key = gemini_api_key)
image_file = "E:\\Python\\RyuKyuGlobal\\GOOGLE_OCR\\Images\\receipt_0.png" ##test image file path


if __name__ =="__main__":
   try:
      result = gemini_ocr.analyze_receipt(image_file = image_file)
      print(result)
   except Exception as e:
      print(e)



