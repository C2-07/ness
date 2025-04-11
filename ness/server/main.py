# import logging
# from fastapi import FastAPI
# import uvicorn
# from api import router

# logging.basicConfig(
#     level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
# )
# logger = logging.getLogger(__name__)

# app = FastAPI(title="Ness API", version="1.0.0")
# app.include_router(router=router, prefix="/api", tags=["api"])

# if __name__ == "__main__":
#     uvicorn.run(app=app, host="127.0.0.1", port=8000, log_level="info")

# Anywhere in your app
from plugins import registered_plugins

response = registered_plugins["hello"].execute(user="Gourav")

