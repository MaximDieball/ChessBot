import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from bots.randomBot.randomBot import get_random_bot_move
from bots.botv1.botv1 import get_botv1_move
from bots.botv2.botv2 import get_botv2_move
from bots.botv3.botv3 import start_botv3_move_search
from bots.botv4.botv4 import start_botv4_move_search
from bots.botv5.botv5 import start_botv5_move_search
from bots.botv6.botv6 import start_botv6_move_search
from bots.botLib.lib import Game as Gamev1
from bots.botLib.libv2 import Game as Gamev2
from bots.botLib.libv3wrapper import Game as Gamev3
import time

app = FastAPI()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_json()
            start_time = time.perf_counter()
            match data["bot"]:
                case "random":
                    game = Gamev1()
                    game.import_board_string(data['board'])
                    move = get_random_bot_move(game, data['turn'])
                case "v1":
                    game = Gamev1()
                    game.import_board_string(data['board'])
                    move = get_botv1_move(game, data['turn'])
                case "v2":
                    game = Gamev1()
                    game.import_board_string(data['board'])
                    move, evaluation = get_botv2_move(game, data['turn'])
                case "v3":
                    game = Gamev2()
                    game.import_board_string(data['board'])
                    move, evaluation = start_botv3_move_search(game, data['turn'])
                case "v4":
                    game = Gamev2()
                    game.import_board_string(data['board'])
                    move, evaluation = start_botv4_move_search(game, data['turn'])
                case "v5":
                    game = Gamev3()
                    game.import_board_string(data['board'])
                    move, evaluation = start_botv5_move_search(game, data['turn'])
                case "v6":
                    game = Gamev3()
                    game.import_board_string(data['board'])
                    move, evaluation = start_botv6_move_search(game, data['turn'])
                case _:
                    game = Gamev2()
                    game.import_board_string(data['board'])
                    move = get_random_bot_move(game, data['turn'])
            # Send the move back to the React app
            await websocket.send_json({"type": "move", "originalPosition": move[0], "newPosition": move[1]})
            end_time = time.perf_counter()
            print(f"{data["bot"]} took : {end_time - start_time:.4f} s")
    except WebSocketDisconnect:
        print("Client disconnected")


# static file/index setup / gpt fix
app.mount("/assets", StaticFiles(directory="../frontend/react-app/dist/assets"), name="assets")


@app.get("/{full_path:path}")
async def serve_react_app(full_path: str):
    build_index = os.path.join("../frontend/react-app/dist", "index.html")
    return FileResponse(build_index)