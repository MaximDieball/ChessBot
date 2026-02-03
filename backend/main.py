import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from bots.randomBot import get_move

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            move = get_move(data['board'], data['turn'])

            # Send the move back to the React app
            await websocket.send_json({"type": "move", "originalPosition": move[0], "newPosition": move[1]})
    except WebSocketDisconnect:
        print("Client disconnected")


# Your existing static file/index setup
app.mount("/assets", StaticFiles(directory="../frontend/react-app/dist/assets"), name="assets")


@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    build_index = os.path.join("../frontend/react-app/dist", "index.html")
    return FileResponse(build_index)