import os
import logging

logger = logging.getLogger(__name__)
# Absolute path to the project root
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPT_DIR = os.path.join(BASE_DIR, "prompts")


def load_prompt(name: str) -> str:
    """Load a single prompt from the prompts directory."""
    
    try:
        path = os.path.join(PROMPT_DIR, f"{name}.txt")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        logging.warning(f"Prompt Doesn't Exists: ness/server/prompts{name}.txt")

def load_all_prompts() -> dict:
    """Load all .txt prompt files from the prompts directory."""
    
    prompts = {}
    for filename in os.listdir(PROMPT_DIR):
        if filename.endswith(".txt"):
            name = filename[:-4]
            prompts[name] = load_prompt(name)
    # Convert keys to lowercase for consistency
    prompts = {key.lower(): value for key, value in prompts.items()}
    return prompts

 