import uvicorn
from app.app import Application

fastapi_app = Application().run()

if __name__ == "__main__":
    uvicorn.run(fastapi_app, host="0.0.0.0", port=8001)