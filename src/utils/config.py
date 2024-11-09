import yaml
from pathlib import Path

def load_config(config_path="src/config/config.yaml"):
    try:
        with open(Path(config_path)) as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Error loading config: {str(e)}")
        return None 