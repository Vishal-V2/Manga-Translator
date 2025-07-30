from pipeline.core.translation.deepseek import DeepseekApi
from pipeline.core.translation.gemini import GeminiApi



class TranslationBase:
    def __init__(self, api_config: dict, translation_config: dict):
        self.selected_api = api_config.get("selected")
        selected_config = api_config.get(self.selected_api, {})
        self.selected_key = selected_config.get("api_key")
        self.selected_model = selected_config.get("model")


        if self.selected_api == "deepseek":
            self.api = DeepseekApi(self.selected_key, self.selected_model)
        elif self.selected_api == "gemini":
            self.api = GeminiApi(self.selected_key, self.selected_model)


    def batch_translation(self, batch_dict: dict) -> dict:
        if self.selected_key is not None:
            batch_dicts = self.api.translate(batch_dict)
            return batch_dicts

      
        