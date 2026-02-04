import { useNavigate } from "react-router-dom"

function HomePage() {
    const navigate = useNavigate()
    const gotToPlayChessBotPage = () => {
        navigate("/play-chess-bot");
};

  return (
    <>
      <div className="d-flex flex-column justify-content-center align-items-center vh-100">
        <h1
          className="position-absolute start-50 translate-middle-x"
          style={{ top: "25%" }}
        >
          Play Against My Custom Chess Bot
        </h1>
        <button
          type="button"
          className="btn btn-primary btn-lg w-25"
          onClick={gotToPlayChessBotPage}
        >
          Play
        </button>
      </div>
    </>
  );
}

export default HomePage;
