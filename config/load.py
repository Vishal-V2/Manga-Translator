import yaml
import constants
import os



def load_config_file() -> dict:
    try:
        if not os.path.exists(constants.CONFIG_FILE):
            raise FileNotFoundError(f"Config file not found: {constants.CONFIG_FILE}")
        
        with open(constants.CONFIG_FILE, "r") as file:
            data = yaml.safe_load(file)
            if not isinstance(data, dict):
                raise ValueError("Config file must contain a top-level dictionary.")
            return data
    except (FileNotFoundError, PermissionError) as e:
        print(f"[CONFIG LOAD ERROR] File error: {e}")
    except yaml.YAMLError as e:
        print(f"[CONFIG LOAD ERROR] YAML parsing error: {e}")
    except Exception as e:
        print(f"[CONFIG LOAD ERROR] Unexpected error: {e}")
        
    return {}


def save_in_config_file(keys, new_value):
    with open(constants.CONFIG_FILE, "r") as file:
        config = yaml.safe_load(file)
    
    data = config
    for key in keys[:-1]:
        data = data.setdefault(key, {})
    data[keys[-1]] = new_value

    with open(constants.CONFIG_FILE, "w") as file:
        yaml.dump(config, file, sort_keys=False)


def save_full_config(section: dict, key: str):
    with open(constants.CONFIG_FILE, "r") as file:
        config = yaml.safe_load(file) or {}

    config[key] = section

    with open(constants.CONFIG_FILE, "w") as file:
        yaml.dump(config, file, sort_keys=False)


def get_config_value(key: str):
    with open(constants.CONFIG_FILE, "r") as file:
        config = yaml.safe_load(file)
    
    return config.get(key)