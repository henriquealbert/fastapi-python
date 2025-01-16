from typing import Union
from contextlib import asynccontextmanager
from fastapi import FastAPI
from gunicorn.app.base import BaseApplication

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code here (if any)
    yield
    # Cleanup code here (if any)
    print("Application shutdown")

app = FastAPI(lifespan=lifespan)

@app.get("/")
def read_root():
    return {"Hello": "World FastAPI"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    class StandaloneApplication(BaseApplication):
        def __init__(self, app, options=None):
            self.options = options or {}
            self.application = app
            super().__init__()

        def load_config(self):
            config = {key: value for key, value in self.options.items()
                     if key in self.cfg.settings and value is not None}
            for key, value in config.items():
                self.cfg.set(key.lower(), value)

        def load(self):
            return self.application

    options = {
        'bind': '0.0.0.0:3000',
        'worker_class': 'uvicorn.workers.UvicornWorker',
        'workers': 1
    }
    StandaloneApplication(app, options).run()