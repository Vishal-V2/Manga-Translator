from config.load import load_config_file


class ConfigBase:
    def __init__(self):
        config = load_config_file()

        self.config_api = config.get("api_group", {})
        self.config_detection = config.get("detection_group", {})
        self.config_cleaning = config.get("cleaning_group", {})
        self.config_translation = config.get("translation_group", {})


    @property
    def api_config(self):
        return self.config_api


    @property
    def detection_config(self):
        return self.config_detection


    @property
    def cleaning_config(self):
        return self.config_cleaning


    @property
    def translation_config(self):
        return self.config_translation