import { BrowserRouter, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import PlayChessBotPage from "./pages/PlayChessBotPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/play-chess-bot" element={<PlayChessBotPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
