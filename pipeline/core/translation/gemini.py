from google import genai
from google.genai.errors import (
    ClientError, ServerError, APIError
)

import json

import constants
from pipeline.core.utility import markdown


class GeminiApi:
    def __init__(self, api_key: str, model: str):
        self.client = genai.Client(api_key=api_key)
        self.model = model
    

    def translate(self, jp_texts_dict: dict) -> dict:
        prompt = constants.CUSTOM_PROMPT_V2
        jp_texts = json.dumps(jp_texts_dict, ensure_ascii=False, indent=4)

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=(prompt + jp_texts)
            )
            tr_texts = response.text

            return self._parse_json(tr_texts)
        
        except ClientError as e:
            error_messages = {
                400: {
                    "INVALID_ARGUMENT": "The request body is malformed. Check the API reference for request format and examples.",
                    "FAILED_PRECONDITION": "Gemini API free tier is not available in your country. Please enable billing on your project in Google AI Studio."
                },
                403: "Your API key doesn't have the required permissions. Check that your API key is set and has the right access.",
                404: "The requested resource wasn't found. Check if all parameters in your request are valid for your API version.",
                429: "You've exceeded the rate limit. You are sending too many requests per minute. Please slow down your requests."
            }
            status_code = e.code
            status_string = getattr(e, "status", "")

            if status_code == 400 and isinstance(error_messages[400], dict):
                if status_string in error_messages[400]:
                    print(error_messages[400][status_string])
                else:
                    print(error_messages[400]["INVALID_ARGUMENT"])
            elif status_code in error_messages:
                print(error_messages[status_code])
            else:
                print(f"Client error {status_code}: {e.message}")

        except ServerError as e:
            error_messages = {
                500: "An unexpected error occurred on Google's side. Your input context might be too long. Try reducing input size or switching to Gemini 1.5 Flash.",
                503: "The service may be temporarily overloaded or down. Try switching to another model or wait and retry.",
                504: "The service is unable to finish processing within the deadline. Your prompt might be too large. Try setting a larger timeout or reducing prompt size."
            }
            status_code = e.code

            if status_code in error_messages:
                print(error_messages[status_code])
            else:
                print(f"Server error {status_code}: {e.message}")

        except APIError as e:
            error_message = f"API Error: {e.message}"
            status_code = getattr(e, 'code', None)
            print(error_message)

        except Exception as e:
            error_message = str(e).lower()

            if any(keyword in error_message for keyword in ["getaddrinfo failed", "name resolution", "dns"]):
                print("NETWORK_CONNECTIVITY_ERROR")
            elif any(keyword in error_message for keyword in ["connection refused", "connection reset", "connection aborted"]):
                print("NETWORK_CONNECTIVITY_ERROR")
            elif any(keyword in error_message for keyword in ["timeout", "timed out"]):
                print("NETWORK_TIMEOUT_ERROR")
            else:
                print("UNEXPECTED_ERROR")

        return {}
    

    def _parse_json(self, text: str) -> dict:
        try:
            stripped_text = markdown.extract_markdown_codeblock(text)
            
            # Clean up whitespace and find JSON start
            cleaned_text = stripped_text.strip()
            
            # Try to fix common JSON formatting issues
            if not cleaned_text.startswith('{'):
                # Find the first { character
                start_idx = cleaned_text.find('{')
                if start_idx != -1:
                    cleaned_text = cleaned_text[start_idx:]
            
            # Parse JSON directly without escaping newlines (they're valid in JSON strings)
            return json.loads(cleaned_text)
        except json.JSONDecodeError as e:
            print("[JSON Decode Error] Invalid response format from Gemini:\n", e)
            print("Raw content:\n", text)
            print("Cleaned content:\n", cleaned_text if 'cleaned_text' in locals() else "N/A")

            return {}
    
