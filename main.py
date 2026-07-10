"""
Entry point – run with:  python main.py
or:  uvicorn recipe_agent.api.app:app --reload
"""
import uvicorn
from recipe_agent.core.config import settings

if __name__ == "__main__":
    uvicorn.run(
        "recipe_agent.api.app:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        reload=settings.DEBUG,
        log_level="debug" if settings.DEBUG else "info",
    )
