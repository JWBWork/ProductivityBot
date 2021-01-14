import json, os
from src.paths import SRC_DIR

config_path = os.path.join(SRC_DIR, '..', 'config.json')
with open(config_path, 'rb') as config_file:
    config = json.load(config_file)

if __name__ == '__main__':
    print(config)
