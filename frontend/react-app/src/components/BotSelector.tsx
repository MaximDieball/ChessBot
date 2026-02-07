import { useState } from "react";
import Carousel from "react-bootstrap/Carousel";
import "bootstrap/dist/css/bootstrap.min.css";

const bots = [
  { id: "random", name: "😵‍💫 Random Bot", desc: "Just plays random moves" },
  {
    id: "v1",
    name: "🤖 Bob",
    desc: "Looks 1 move ahead",
  },
  {
    id: "v2",
    name: "🤖 Bobs Older Brother",
    desc: "Looks 5 move ahead",
  },
];

interface BotSelectorProps {
  onSelectBot: (botId: string) => void;
}

function BotSelector({ onSelectBot }: BotSelectorProps) {
  const [index, setIndex] = useState(0);

  const handleSelect = (selectedIndex: number) => {
    setIndex(selectedIndex);
    onSelectBot(bots[selectedIndex].id);
  };

  return (
    <div className="w-100 bg-light">
      <Carousel
        activeIndex={index}
        onSelect={handleSelect}
        variant="dark"
        interval={null}
        indicators={false}
        style={{ height: "80px", backgroundColor: "white" }}
      >
        {bots.map((bot) => (
          <Carousel.Item key={bot.id} style={{ height: "80px" }}>
            <div
              className="d-flex flex-column align-items-center justify-content-center h-100"
              style={{ cursor: "pointer" }}
            >
              <h5 className="fw-bold m-0"> {bot.name}</h5>
              <small className="text-muted">{bot.desc}</small>
            </div>
          </Carousel.Item>
        ))}
      </Carousel>
    </div>
  );
}

export default BotSelector;
