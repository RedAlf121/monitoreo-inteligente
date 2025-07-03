from dotenv import load_dotenv
import os
__all__ = ["init_env_vars","get_env_vars"]
env_vars = {}

def get_env_vars_from_dotenv(dotenv_path='.env'):
    load_dotenv(dotenv_path)

    env_keys = set()
    with open(dotenv_path) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key = line.split('=', 1)[0].strip()
                env_keys.add(key)

    env_vars = {key: os.environ[key] for key in env_keys if key in os.environ}
    return env_vars 

def init_env_vars():
    global env_vars
    env_vars = get_env_vars_from_dotenv()

def get_env_vars():
    return env_vars
