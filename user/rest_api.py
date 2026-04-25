from contextlib import asynccontextmanager

import uvicorn
import config

from fastapi import FastAPI, Query
from engine import Engine

from .models import Script


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 🔥 startup logic

    app.state.engine = Engine(series_data_path=config.SERIES_DATA_PATH,
                              output_data_path=config.OUTPUT_ROOT_PATH)

    yield


app = FastAPI(lifespan=lifespan)

@app.get('/')
def root():
    return {"Health Check": "I am alive"}

@app.post('/execute')
def root(script: Script):
    user_script = script.script
    engine = app.state.engine
    try:
        output_id = engine.run_engine(user_script)
    except:
        return {"message": "Invalid script"}
    return {"message": "Script successfully executed",
            "result": output_id}


@app.get('/view/{run_id}')
def root(run_id: str, items: list[str] = Query(...)):
    engine = app.state.engine
    try:
        res = engine.view(run_id, items)
    except (FileNotFoundError, KeyError):
        return {"message": "Invalid input"}

    return res

if __name__ == "__main__":
    uvicorn.run("user.rest_api:app", host="127.0.0.1", port=8000, reload=True)