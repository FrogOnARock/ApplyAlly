import os
from dotenv import load_dotenv

load_dotenv()

AGENT_NAME = "brand_search_optimization"
DESCRIPTION = "A helpful assistant for brand search optimization."
PROJECT = os.getenv("GOOGLE_CLOUD_PROJECT", "EMPTY")
LOCATION = os.getenv("GOOGLE_CLOUD_LOCATION", "global")
GOOGLE_MODEL = os.getenv("MODEL", "gemini-2.0-flash")
OPENAI_MODEL = os.getenv("OPENAIMODEL", "openai/gpt-4.1")
DISABLE_WEB_DRIVER = int(os.getenv("DISABLE_WEB_DRIVER", "0"))
WHL_FILE_NAME = os.getenv("ADK_WHL_FILE", "")
STAGING_BUCKET = os.getenv("STAGING_BUCKET", "")
OPENAI_CLIENTKEY = os.getenv("OPEN_AI_API_KEY", None)