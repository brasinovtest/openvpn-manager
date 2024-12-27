from fastapi import FastAPI

def create_app():
    app = FastAPI()
    from routes import status
    app.include_router(status)
    return app