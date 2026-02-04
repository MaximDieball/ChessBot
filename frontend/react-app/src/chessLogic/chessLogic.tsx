let board = Array(64).fill("");
let legalMoves = Array(64).fill(0);
let turn = "w";
let wKPos = 60;
let bKPos = 4;
let inCheck = false;
let movesOutOfCheck: number[][] = [];
let winner = "";

export function movePiece(originalPosition: number, newPosition: number) {
  const piece = board[originalPosition];
  const pieceType = piece.substring(0, 3);
  const moves = Number(piece.slice(4)) + 1;
  const pieceTaken = board[newPosition];
  board[newPosition] = pieceType + "-" + moves;
  board[originalPosition] = "";
  // tracking King
  if (pieceType === "w-K") {
    wKPos = newPosition;
  } else if (pieceType == "b-K") {
    bKPos = newPosition;
  }
  // castle logic
  if (pieceType === "w-K" && newPosition === 62) {
    movePiece(63, 61); // move rook
  }
  if (pieceType === "w-K" && newPosition === 58) {
    movePiece(56, 59); // move rook
  }
  if (pieceType === "b-K" && newPosition === 2) {
    movePiece(0, 3); // move rook
  }
  if (pieceType === "b-K" && newPosition === 6) {
    movePiece(7, 5); // move rook
  }

  // en passant
  if (pieceType === "b-P" && newPosition - originalPosition === 16) {
    board[newPosition - 8] = "b-E-0";
  }
  if (pieceType === "w-P" && originalPosition - newPosition === 16) {
    board[newPosition + 8] = "w-E-0";
  }
  if (pieceTaken === "b-E-0") {
    board[newPosition + 8] = "";
  }
  if (pieceTaken === "w-E-0") {
    board[newPosition - 8] = "";
  }
  console.log("moved Piece");
  switchTurn();
}

function simulateMoveOutOfCheck(
  originalPosition: number,
  newPosition: number,
  board: string[],
) {
  let simulatedBoard = [...board];
  const piece = simulatedBoard[originalPosition];
  const pieceType = piece.substring(0, 3);
  const moves = Number(piece.slice(4)) + 1;
  const pieceTaken = simulatedBoard[newPosition];
  simulatedBoard[newPosition] = pieceType + "-" + moves;
  simulatedBoard[originalPosition] = "";

  // en passant
  if (pieceType === "b-P" && newPosition - originalPosition === 16) {
    simulatedBoard[newPosition - 8] = "b-E-0";
  }
  if (pieceType === "w-P" && originalPosition - newPosition === 16) {
    simulatedBoard[newPosition + 8] = "w-E-0";
  }
  if (pieceTaken === "b-E-0") {
    simulatedBoard[newPosition + 8] = "";
  }
  if (pieceTaken === "w-E-0") {
    simulatedBoard[newPosition - 8] = "";
  }
  return simulatedBoard;
}

export function getBoard() {
  return board;
}
export function getLegalMoves() {
  return legalMoves;
}
export function getTurn() {
  return turn;
}

export function getWinner(){
    return winner;
}

function straightRay(start: number, delta: number, inputBoard: string[]) {
  let board = [...inputBoard];
  let square = start;
  let foundSquares: number[] = [];
  // check edge cases when bishop is on the edge of the board
  if (
    (delta === 8 && square > 55) ||
    (delta === -8 && square < 8) ||
    (delta === -1 && square % 8 === 0) ||
    (delta === 1 && square % 8 === 7)
  ) {
    return foundSquares;
  }

  for (let steps = 0; steps < 7; steps++) {
    // next square
    square = square + delta;
    // remove enpassant pieces
    if (board[square] !== "" && board[square][2] === "E") {
      board[square] = "";
    }
    // enemy piece
    if (board[square] !== "" && board[square][0] !== turn) {
      foundSquares.push(square);
      return foundSquares;
    }
    // own piece
    if (board[square] !== "") {
      return foundSquares;
    }
    // border
    if ((square > 55 && delta === 8) || (square < 8 && delta === -8)) {
      foundSquares.push(square);
      return foundSquares;
    }
    if (
      (square % 8 === 7 && delta === 1) ||
      (square % 8 === 0 && delta === -1)
    ) {
      foundSquares.push(square);
      return foundSquares;
    }
    // empty square
    foundSquares.push(square);
  }
  return foundSquares;
}

function diagonalRay(start: number, delta: number, inputBoard: string[]) {
  let board = [...inputBoard];
  let square = start;
  let foundSquares: number[] = [];
  // check edge cases when bishop is on the edge of the board
  if ((delta > 0 && square > 55) || (delta < 0 && square < 8)) {
    return foundSquares;
  }
  if (
    ((delta === -9 || delta === 7) && square % 8 === 0) ||
    ((delta === 9 || delta === -7) && square % 8 === 7)
  ) {
    return foundSquares;
  }

  for (let steps = 0; steps < 7; steps++) {
    // next square
    square = square + delta;
    // remove enpassant pieces
    if (board[square] !== "" && board[square][2] === "E") {
      board[square] = "";
    }
    // enemy piece
    if (board[square] !== "" && board[square][0] !== turn) {
      foundSquares.push(square);
      return foundSquares;
    }
    // own piece
    if (board[square] !== "") {
      return foundSquares;
    }
    // border
    if (square > 55 || square < 8) {
      foundSquares.push(square);
      return foundSquares;
    }
    if (square % 8 === 7 || square % 8 === 0) {
      foundSquares.push(square);
      return foundSquares;
    }
    // empty square
    foundSquares.push(square);
  }
  return foundSquares;
}

function findKingMoves(position: number, board: string[]) {
  let foundSquares: number[] = [];
  if (position > 7) {
    (board[position - 8] === "" || board[position - 8][0] !== turn) &&
      foundSquares.push(position - 8);
    if (position % 8 !== 7) {
      (board[position + 1] === "" || board[position + 1][0] !== turn) &&
        foundSquares.push(position + 1);
      (board[position + 1 - 8] === "" || board[position + 1 - 8][0] !== turn) &&
        foundSquares.push(position + 1 - 8);
    }
    if (position % 8 !== 0) {
      (board[position - 1] === "" || board[position - 1][0] !== turn) &&
        foundSquares.push(position - 1);
      (board[position - 1 - 8] === "" || board[position - 1 - 8][0] !== turn) &&
        foundSquares.push(position - 1 - 8);
    }
  }
  if (position < 56) {
    (board[position + 8] === "" || board[position + 8][0] !== turn) &&
      foundSquares.push(position + 8);

    if (position % 8 !== 7) {
      (board[position + 1] === "" || board[position + 1][0] !== turn) &&
        foundSquares.push(position + 1);
      (board[position + 1 + 8] === "" || board[position + 1 + 8][0] !== turn) &&
        foundSquares.push(position + 1 + 8);
    }
    if (position % 8 !== 0) {
      (board[position - 1] === "" || board[position - 1][0] !== turn) &&
        foundSquares.push(position - 1);
      (board[position - 1 + 8] === "" || board[position - 1 + 8][0] !== turn) &&
        foundSquares.push(position - 1 + 8);
    }
  }
  return foundSquares;
}

function isOpponentQueenOrRook(position: number | undefined, color: string) {
  if (position === undefined) {
    return false;
  }
  let piece = board[position];
  if (
    piece !== "" &&
    (piece[2] === "R" || piece[2] === "Q") &&
    piece[0] !== color
  ) {
    return true;
  }
  return false;
}
function isOpponentQueenOrBishop(position: number | undefined, color: string) {
  if (position === undefined) {
    return false;
  }
  let piece = board[position];
  if (
    piece !== "" &&
    (piece[2] === "B" || piece[2] === "Q") &&
    piece[0] !== color
  ) {
    return true;
  }
  return false;
}

function checkMate(color: string, position: number, board: string[]) {
  inCheck = checkCheck(color, position, board);

  if (inCheck) {
    // find all legal moves
    let possibleMoves: number[][] = [];
    for (let pos = 0; pos < 64; pos++) {
      if (board[pos] !== "" && board[pos][0] === color) {
        let legalMovesFound = findLegalMoves(pos, board[pos], board);
        for (let move = 0; move < legalMovesFound.length; move++) {
          possibleMoves.push([pos, legalMovesFound[move]]);
        }
      }
    }
    // check if a move can move color out of check
    let inMate = true;
    movesOutOfCheck = [];
    for (let i = 0; i < possibleMoves.length; i++) {
      let simulatedBoard = simulateMoveOutOfCheck(
        possibleMoves[i][0],
        possibleMoves[i][1],
        board,
      );
      let kingPosInSim = position;
      if (board[possibleMoves[i][0]][2] === "K") {
        kingPosInSim = possibleMoves[i][1];
      }
      if (checkCheck(color, kingPosInSim, simulatedBoard) === false) {
        inMate = false;
        movesOutOfCheck.push(possibleMoves[i]);
      }
    }
    return inMate;
  }
  return false;
}

function checkCheck(color: string, position: number, board: string[]) {
  const knightSquares = findKnightMoves(position, board);
  let knightCheck = false;
  for (let i = 0; i < knightSquares.length; i++) {
    let piece = board[knightSquares[i]];
    if (piece !== "" && piece[0][3] === "N" && piece[0] !== color) {
      knightCheck = true;
    }
  }

  let rookCheck =
    isOpponentQueenOrRook(straightRay(position, 1, board).at(-1), color) ||
    isOpponentQueenOrRook(straightRay(position, -1, board).at(-1), color) ||
    isOpponentQueenOrRook(straightRay(position, 8, board).at(-1), color) ||
    isOpponentQueenOrRook(straightRay(position, -8, board).at(-1), color);

  let bishopCheck =
    isOpponentQueenOrBishop(diagonalRay(position, -7, board).at(-1), color) ||
    isOpponentQueenOrBishop(diagonalRay(position, 7, board).at(-1), color) ||
    isOpponentQueenOrBishop(diagonalRay(position, -9, board).at(-1), color) ||
    isOpponentQueenOrBishop(diagonalRay(position, 9, board).at(-1), color);

  let pawnCheck =
    // check for pawn checks
    (color === "b" &&
      board[position + 7] !== "" &&
      board[position + 7].substring(0, 3) === "w-P") ||
    (color === "b" &&
      board[position + 9] !== "" &&
      board[position + 9].substring(0, 3) === "w-P") ||
    (color === "w" &&
      board[position - 7] !== "" &&
      board[position - 7].substring(0, 3) === "b-P") ||
    (color === "w" &&
      board[position - 9] !== "" &&
      board[position - 9].substring(0, 3) === "b-P");

  // "king check"
  let kingCheck = false;
  let kingMoves = findKingMoves(position, legalMoves);
  for (let i = 0; i < kingMoves.length; i++) {
    if (
      board[kingMoves[i]] !== "" &&
      board[kingMoves[i]][0] !== color &&
      board[kingMoves[i]][2] === "K"
    ) {
      kingCheck = true;
    }
  }

  return pawnCheck || knightCheck || bishopCheck || rookCheck || kingCheck;
}

function findKnightMoves(position: number, board: string[]) {
  let foundSquares: number[] = [];
  if (position > 15) {
    if (position % 8 !== 0) {
      (board[position - 16 - 1] === "" ||
        board[position - 16 - 1][0] !== turn) &&
        foundSquares.push(position - 16 - 1);
    }
    if (position % 8 !== 7) {
      (board[position - 16 + 1] === "" ||
        board[position - 16 + 1][0] !== turn) &&
        foundSquares.push(position - 16 + 1);
    }
  }

  if (position < 48) {
    if (position % 8 !== 0) {
      foundSquares.push(position + 16 - 1);
      (board[position + 16 - 1] === "" ||
        board[position + 16 - 1][0] !== turn) &&
        foundSquares.push(position + 16 - 1);
    }
    if (position % 8 !== 7) {
      foundSquares.push(position + 16 + 1);
      (board[position + 16 + 1] === "" ||
        board[position + 16 + 1][0] !== turn) &&
        foundSquares.push(position + 16 + 1);
    }
  }

  if (position % 8 > 1) {
    if (position > 7) {
      (board[position - 8 - 2] === "" || board[position - 8 - 2][0] !== turn) &&
        foundSquares.push(position - 8 - 2);
    }
    if (position < 56) {
      (board[position + 8 - 2] === "" || board[position + 8 - 2][0] !== turn) &&
        foundSquares.push(position + 8 - 2);
    }
  }

  if (position % 8 < 6) {
    if (position > 7) {
      (board[position - 8 + 2] === "" || board[position - 8 + 2][0] !== turn) &&
        foundSquares.push(position - 8 + 2);
    }
    if (position < 56) {
      (board[position + 8 + 2] === "" || board[position + 8 + 2][0] !== turn) &&
        foundSquares.push(position + 8 + 2);
    }
  }
  return foundSquares;
}

export function loadLegalMoves(position: number, pieceWithFlag: string) {
  let foundMoves: number[] = [];
  if (inCheck === false) {
    foundMoves = findLegalMoves(position, pieceWithFlag, board);
  } else {
    console.log("out of check moves: " + movesOutOfCheck.length);
    for (let i = 0; i < movesOutOfCheck.length; i++) {
      console.log(
        "move " + movesOutOfCheck[i][0] + " to " + movesOutOfCheck[i][1],
      );
      if (movesOutOfCheck[i][0] === position) {
        foundMoves.push(movesOutOfCheck[i][1]);
        console.log("");
      }
    }
  }

  legalMoves = Array(64).fill(0);
  for (let i = 0; i < 64; i++) {
    legalMoves[foundMoves[i]] = 1;
  }
}

function findLegalMoves(
  position: number,
  pieceWithFlag: string,
  board: string[],
) {
  // select all squares for now
  console.log(pieceWithFlag);
  console.log(position);
  let foundMoves: number[] = [];
  // implement cheat here
  const pieceType = pieceWithFlag.substring(0, 3);
  switch (pieceType) {
    case "w-P":
      // move up one sqare
      if (board[position - 8] === "") {
        foundMoves.push(position - 8);
      }
      // move two sqares
      if (board[position - 16] === "" && position > 47 && position < 56) {
        foundMoves.push(position - 16);
      }
      // take diagonal
      if ( position % 8 !== 0 && board[position - 9] !== "" && board[position - 9][0] === "b") {
        foundMoves.push(position - 9);
      }
      if (position % 8 !== 7 && board[position -7] !== "" && board[position - 7][0] === "b") {
        foundMoves.push(position - 7);
      }
      break;

    case "b-P":
      // move up one sqare
      if (board[position + 8] === "") {
        foundMoves.push(position + 8);
      }
      // move two sqares
      if (board[position + 16] === "" && position > 7 && position < 16) {
        foundMoves.push(position + 16);
      }
      // take diagonal
      if (position % 8 !== 7 && board[position + 9] !== "" && board[position + 9][0] === "w") {
        foundMoves.push(position + 9);
      }
      if (position % 8 !== 0 && board[position + 7] !== "" && board[position + 7][0] === "w") {
        foundMoves.push(position + 7);
      }
      break;

    case "w-B":
    case "b-B":
      foundMoves.push(...diagonalRay(position, -7, board));
      foundMoves.push(...diagonalRay(position, 7, board));
      foundMoves.push(...diagonalRay(position, -9, board));
      foundMoves.push(...diagonalRay(position, 9, board));
      break;
    case "w-R":
    case "b-R":
      foundMoves.push(...straightRay(position, 1, board));
      foundMoves.push(...straightRay(position, -1, board));
      foundMoves.push(...straightRay(position, 8, board));
      foundMoves.push(...straightRay(position, -8, board));
      break;
    case "w-Q":
    case "b-Q":
      foundMoves.push(...straightRay(position, 1, board));
      foundMoves.push(...straightRay(position, -1, board));
      foundMoves.push(...straightRay(position, 8, board));
      foundMoves.push(...straightRay(position, -8, board));

      foundMoves.push(...diagonalRay(position, -7, board));
      foundMoves.push(...diagonalRay(position, 7, board));
      foundMoves.push(...diagonalRay(position, -9, board));
      foundMoves.push(...diagonalRay(position, 9, board));
      break;

    case "w-N":
    case "b-N":
      foundMoves.push(...findKnightMoves(position, board));
      break;

    case "w-K":
      // check castle
      if (
        pieceWithFlag.substring(4, 5) === "0" &&
        board[63] === "w-R-0" &&
        board[62] === "" &&
        board[61] === ""
      ) {
        foundMoves.push(62);
      }
      if (
        pieceWithFlag.substring(4, 5) === "0" &&
        board[56] === "w-R-0" &&
        board[57] === "" &&
        board[58] === "" &&
        board[59] === ""
      ) {
        foundMoves.push(58);
      }
      foundMoves.push(...findKingMoves(position, board));
      break;
    case "b-K":
      // check castle
      if (
        pieceWithFlag.substring(4, 5) === "0" &&
        board[7] === "b-R-0" &&
        board[6] === "" &&
        board[5] === ""
      ) {
        foundMoves.push(6);
      }
      if (
        pieceWithFlag.substring(4, 5) === "0" &&
        board[0] === "b-R-0" &&
        board[1] === "" &&
        board[2] === "" &&
        board[3] === ""
      ) {
        foundMoves.push(2);
      }
      foundMoves.push(...findKingMoves(position, board));
      break;
    // TODO check for checks / and checkmate
    default:
      foundMoves = Array(64).fill(1);
  }
  return foundMoves;
}

function removeEnpassantPieces(color: string) {
  if (color === "b") {
    for (let i = 15; i < 24; i++) {
      if (board[i] === "b-E-0") {
        board[i] = "";
      }
    }
  } else {
    for (let i = 40; i < 48; i++) {
      if (board[i] === "w-E-0") {
        board[i] = "";
      }
    }
  }
}
export function resetLegalMoves() {
  legalMoves = Array(64).fill(0);
}

function switchTurn() {
  if (turn == "w") {
    turn = "b";
    removeEnpassantPieces("b");
    let inMate = checkMate("b", bKPos, board);
    console.log("inMate: " + inMate);
    console.log("inCheck: " + inCheck);
    if (inMate === true) {
      winner = "w";
    }
    // pop up
  } else {
    turn = "w";
    removeEnpassantPieces("w");
    let inMate = checkMate("w", wKPos, board);
    console.log("inMate: " + inMate);
    console.log("inCheck: " + inCheck);
    if (inMate === true) {
      winner = "b";
    }
    // pop up
  }
}

export function resetBoard() {
  //setSelectedSquare(-1);
  resetLegalMoves();
  turn = "w";
  board = Array(64).fill("");
  inCheck = false;
  movesOutOfCheck = [];
  winner = "";

  // black pieces
  board[0] = "b-R-0";
  board[1] = "b-N-0";
  board[2] = "b-B-0";
  board[3] = "b-Q-0";
  board[4] = "b-K-0";
  bKPos = 4;
  board[5] = "b-B-0";
  board[6] = "b-N-0";
  board[7] = "b-R-0";
  for (let i = 8; i <= 15; i++) board[i] = "b-P-0";

  // white pieces
  for (let i = 48; i <= 55; i++) board[i] = "w-P-0";
  board[56] = "w-R-0";
  board[57] = "w-N-0";
  board[58] = "w-B-0";
  board[59] = "w-Q-0";
  board[60] = "w-K-0";
  wKPos = 60;
  board[61] = "w-B-0";
  board[62] = "w-N-0";
  board[63] = "w-R-0";
}
