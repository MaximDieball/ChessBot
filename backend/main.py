import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

app = FastAPI()

app.mount("/assets", StaticFiles(directory="../frontend/react-app/dist/assets"), name="assets")


@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    build_index = os.path.join("../frontend/react-app/dist", "index.html")
    return FileResponse(build_index)
