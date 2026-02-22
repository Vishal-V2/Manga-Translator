from openai import OpenAI
from openai import (
    APIError,
    APITimeoutError,
    APIConnectionError,
    AuthenticationError,
    BadRequestError,
    InternalServerError,
    RateLimitError
)

import json

import constants
from pipeline.core.utility import markdown



class GroqApi:
    def __init__(self, api_key: str, model: str):
        base_url = "https://api.groq.com/openai/v1"
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model
    

    def translate(self, jp_texts_dict: dict) -> dict:
        prompt = constants.CUSTOM_PROMPT_V1 
        jp_texts = json.dumps(jp_texts_dict, ensure_ascii=False, indent=4)

        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": jp_texts}
                ],
                temperature=0.7,
                stream=False
            )

            tr_texts = response.choices[0].message.content
            print("TR TEXT: ", tr_texts)

            return self._parse_json(tr_texts)
        
        except BadRequestError as e:
            print("400 - Invalid Format: Modify your request body. Check API docs.")
            print(f"Error details: {e}")

        except AuthenticationError as e:
            print("401 - Authentication Failed: Check your API key.")

        except APIError as e:
            code = getattr(e, "status_code", "???")

            match code:
                case 402:
                    print("[402] Insufficient Balance: Top up your account.\n", e)
                case 422:
                    print("[422] Invalid Parameters: Check inputs. See docs.\n", e)
                case 503:
                    print("[503] Server Overloaded: Try again later.\n", e)
                case _:
                    print(f"[{code}] Unexpected API error.\n", e)

        except RateLimitError as e:
            print("429 - Rate Limit Reached: Slow down your requests.")

        except InternalServerError as e:
            print("500 - Server Error: Retry after a moment.")

        except APIConnectionError as e:
            print("Network Error: Could not reach Groq server.")

        except Exception as e:
            print("Unexpected error during translation.")
            print(e)
        
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
            print("[JSON Decode Error] Invalid response format from Groq:\n", e)
            print("Raw content:\n", text)
            print("Cleaned content:\n", cleaned_text if 'cleaned_text' in locals() else "N/A")

            return {}
