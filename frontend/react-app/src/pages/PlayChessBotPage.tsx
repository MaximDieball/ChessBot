import { useEffect, useState } from "react";
import {
  resetBoard,
  movePiece,
  loadLegalMoves,
  getBoard,
  getLegalMoves,
  resetLegalMoves,
  getTurn,
  getWinner,
} from "../chessLogic/chessLogic";

import wRook from "../assets/pieces/white-rook.png";
import wBishop from "../assets/pieces/white-bishop.png";
import wKnight from "../assets/pieces/white-knight.png";
import wKing from "../assets/pieces/white-king.png";
import wQueen from "../assets/pieces/white-queen.png";
import wPawn from "../assets/pieces/white-pawn.png";

import bRook from "../assets/pieces/black-rook.png";
import bBishop from "../assets/pieces/black-bishop.png";
import bKnight from "../assets/pieces/black-knight.png";
import bKing from "../assets/pieces/black-king.png";
import bQueen from "../assets/pieces/black-queen.png";
import bPawn from "../assets/pieces/black-pawn.png";

let color = "w";

function PlayChessBotPage() {
  const [selectedSquare, setSelectedSquare] = useState(-1);
  const [, forceRender] = useState(0);
  const [showPopUp, setShowPopUp] = useState(false);
  const [socket, setSocket] = useState<WebSocket | null>(null);

  function onSquareClicked(position: number) {
    const board = getBoard();
    const turn = getTurn();
    const piece = board[position];
    const legalMoves = getLegalMoves();

    if (turn !== color) {
      return;
    }

    if (selectedSquare === -1) {
      if (piece !== "" && piece[0] === turn) {
        // select piece
        loadLegalMoves(position, piece);
        setSelectedSquare(position);
      } else {
        // reset selection
        setSelectedSquare(-1);
        resetLegalMoves();
      }
    } else {
      if (legalMoves[position] === 1) {
        // perform actual move
        movePiece(selectedSquare, position);
        setSelectedSquare(-1);
        resetLegalMoves();
        if (getWinner() !== "") {
          setShowPopUp(true);
          return;
        }
        // send new position to server
        sendMessage(getBoard());
      } else {
        // reset selection
        setSelectedSquare(-1);
        resetLegalMoves();
      }
    }
  }

  function renderPiece(pieceWithFlag: string) {
    const pieceType = pieceWithFlag.substring(0, 3);
    switch (pieceType) {
      // white pieces
      case "w-R":
        return (
          <img
            src={wRook}
            alt="rook"
            style={{ width: "70%", height: "70%", objectFit: "contain" }}
          />
        );
      case "w-B":
        return (
          <img
            src={wBishop}
            alt="bishop"
            style={{ width: "70%", height: "70%", objectFit: "contain" }}
          />
        );
      case "w-N":
        return (
          <img
            src={wKnight}
            alt="knight"
            style={{ width: "70%", height: "70%", objectFit: "contain" }}
          />
        );
      case "w-K":
        return (
          <img
            src={wKing}
            alt="king"
            style={{ width: "70%", height: "70%", objectFit: "contain" }}
          />
        );
      case "w-Q":
        return (
          <img
            src={wQueen}
            alt="queen"
            style={{ width: "70%", height: "70%", objectFit: "contain" }}
          />
        );
      case "w-P":
        return (
          <img
            src={wPawn}
            alt="pawn"
            style={{ width: "70%", height: "70%", objectFit: "contain" }}
          />
        );
      // black pieces
      case "b-R":
        return (
          <img
            src={bRook}
            alt="rook"
            style={{ width: "70%", height: "70%", objectFit: "contain" }}
          />
        );
      case "b-B":
        return (
          <img
            src={bBishop}
            alt="bishop"
            style={{ width: "70%", height: "70%", objectFit: "contain" }}
          />
        );
      case "b-N":
        return (
          <img
            src={bKnight}
            alt="knight"
            style={{ width: "70%", height: "70%", objectFit: "contain" }}
          />
        );
      case "b-K":
        return (
          <img
            src={bKing}
            alt="king"
            style={{ width: "70%", height: "70%", objectFit: "contain" }}
          />
        );
      case "b-Q":
        return (
          <img
            src={bQueen}
            alt="queen"
            style={{ width: "70%", height: "70%", objectFit: "contain" }}
          />
        );
      case "b-P":
        return (
          <img
            src={bPawn}
            alt="pawn"
            style={{ width: "70%", height: "70%", objectFit: "contain" }}
          />
        );
      case "b-E":
      case "w-E":
        return <div>○</div>;
      default:
        return <div></div>;
    }
  }
  function resetBoardButton() {
    setSelectedSquare(-1);
    resetBoard();
    forceRender((n) => n + 1);
    setShowPopUp(false);
  }

  function handleMessage(event: MessageEvent<any>){
    console.log("got Message");
    forceRender((n) => n + 1);
    const response = JSON.parse(event.data);
    if(response["type"] === "move"){
      movePiece(response["originalPosition"], response["newPosition"]);
    }
  }

  function sendMessage(board: string[]){
    console.log("send message");
    socket?.send(JSON.stringify({ "board": board, "turn": getTurn()}));
  }

  useEffect(() => {
    resetBoardButton();
    // start connection
    const ws = new WebSocket("ws://localhost:8000/ws");

    ws.onopen = () => console.log("Connected to Bot");
    ws.onmessage = handleMessage;
    ws.onclose = () => console.log("Disconnected");

    setSocket(ws);
    // Clean up on unmount
    return () => ws.close();
  }, []);

  return (
    <>
      <div className="d-flex flex-column justify-content-center align-items-center vh-100">
        <div
          className="rounded"
          style={{
            width: "min(80vmin, 90vw, 90vh)",
            height: "min(80vmin, 90vw, 90vh)",
            aspectRatio: "1 / 1",
            display: "grid",
            gridTemplateColumns: "repeat(8, 1fr)",
            overflow: "hidden",
            outline: "2px solid black",
          }}
        >
          {getBoard().map((piece, i) => {
            const row = Math.floor(i / 8);
            const col = i % 8;
            const isWhite = row % 2 === 0 ? i % 2 === 0 : i % 2 !== 0;

            return (
              <div
                key={i}
                onClick={() => onSquareClicked(i)}
                style={{
                  aspectRatio: "1 / 1",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  backgroundColor: isWhite ? "#eeeed2" : "#565c96",
                  userSelect: "none",
                  cursor: "pointer",
                  border: selectedSquare === i ? "4px solid #0d6efd" : "",
                }}
              >
                {renderPiece(piece)}
                {
                  <div
                    style={{
                      width: 20,
                      height: 20,
                      position: "absolute",
                      borderRadius: "50%",
                      backgroundColor:
                        getLegalMoves()[i] === 1
                          ? "rgba(25, 25, 25, 0.3)"
                          : "rgba(0, 0, 0, 0)",
                    }}
                  />
                }
              </div>
            );
          })}
        </div>

        <button className="btn btn-primary mt-3" onClick={resetBoardButton}>
          Reset
        </button>
      </div>
      {showPopUp && (
        <div
          className="d-flex flex-column justify-content-center align-items-center"
          style={{
            width: "230px",
            height: "130px",
            position: "fixed",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            backgroundColor: "rgba(42, 42, 42, 0.98)",
            color: "white",
            borderRadius: "10px",
          }}
        >
          <>{getWinner() === "w" ? "White" : "Black"} won the game!</>
          <button
            className="btn btn-primary mt-3"
            onClick={() => setShowPopUp(false)}
          >
            Ok
          </button>
        </div>
      )}
    </>
  );
}

export default PlayChessBotPage;
