import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from bots.randomBot.randomBot import get_random_bot_move
from bots.botv1.botv1 import get_botv1_move
from bots.botv2.botv2 import get_botv2_move

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            match data["bot"]:
                case "random":
                    move = get_random_bot_move(data['board'], data['turn'])
                case "v1":
                    move = get_botv1_move(data['board'], data['turn'])
                case "v2":
                    move, evaluation = get_botv2_move(data['board'], data['turn'])
                case _:
                    move = get_random_bot_move(data['board'], data['turn'])

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