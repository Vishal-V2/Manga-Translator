from pipeline.core.translation.deepseek import DeepseekApi
from pipeline.core.translation.gemini import GeminiApi



class TranslationBase:
    def __init__(self, api_config: dict, translation_config: dict):
        self.api_config = api_config
        self.primary_api = api_config.get("selected")
        
        # Initialize both APIs if keys are available
        self.apis = {}
        
        # Setup Gemini API
        gemini_config = api_config.get("gemini", {})
        gemini_key = gemini_config.get("api_key")
        if gemini_key:
            self.apis["gemini"] = GeminiApi(gemini_key, gemini_config.get("model"))
            
        # Setup DeepSeek API  
        deepseek_config = api_config.get("deepseek", {})
        deepseek_key = deepseek_config.get("api_key")
        if deepseek_key:
            self.apis["deepseek"] = DeepseekApi(deepseek_key, deepseek_config.get("model"))
        
        print(f"Available APIs: {list(self.apis.keys())}")
        print(f"Primary API: {self.primary_api}")


    def batch_translation(self, batch_dict: dict) -> dict:
        if not self.apis:
            print("No API keys provided for translation")
            return batch_dict
            
        # Try primary API first
        if self.primary_api in self.apis:
            print(f"Attempting translation with primary API: {self.primary_api}")
            result = self._try_translation(self.primary_api, batch_dict)
            if result:
                return result
                
        # Try fallback APIs
        for api_name, api_instance in self.apis.items():
            if api_name != self.primary_api:
                print(f"Primary API failed, trying fallback: {api_name}")
                result = self._try_translation(api_name, batch_dict)
                if result:
                    return result
                    
        print("All APIs failed, returning original batch")
        return batch_dict
        
    def _try_translation(self, api_name: str, batch_dict: dict) -> dict:
        try:
            api_instance = self.apis[api_name]
            result = api_instance.translate(batch_dict)
            
            # Check if translation was successful (non-empty result)
            if result and len(result) > 0:
                print(f"✓ {api_name} API succeeded: {len(result)} items translated")
                return result
            else:
                print(f"✗ {api_name} API returned empty result")
                return None
                
        except Exception as e:
            print(f"✗ {api_name} API failed with exception: {str(e)}")
            return None
        