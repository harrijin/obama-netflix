import "./DayColumn.css";
import Card from "react-bootstrap/Card";
import { Col } from "react-bootstrap";

export default function DayColumn({ dayName, dayIndex, tasks }) {
  const ROUND = 3;
  const hours = [];
  console.log(tasks);
  const taskElems = tasks
    ? tasks
        .filter((task) => task.start_time[0] == dayIndex)
        .map((task, i) => {
          const chunk = (window.innerHeight - ROUND * 2) / 25;
          const h = (task.duration / 60) * chunk;
          const y = (task.start_time[1] / 60 + 1) * chunk;

          return (
            <div
              key={i}
              style={{
                backgroundColor: "red",
                position: "absolute",
                top: y,
                height: h,
                width: "100%",
              }}
            >
              {task.name}
            </div>
          );
        })
    : [];
  // const taskElems = []

  for (let i = 0; i < 25; i++) {
    const h = (window.innerHeight - ROUND * 2) / 25;

    hours.push(
      <div
        key={i}
        style={{
          height: h,
          backgroundColor: i == 0 ? "transparent" : "lightblue",
          borderBottom: i == 24 ? "0px" : "1px solid white",
          textAlign: "left",
          borderTop: (i - 1) % 3 == 0 ? '1px solid gray' : ''
        }}
      >
        {getCellContent(dayName, i)}
      </div>
    );
  }

  return (
    <Col style={{ padding: 0 }}>
      <Card className="day-column">
        <Card.Body style={{ padding: 0, backgroundColor: "gray" }}>
          {hours}
          {taskElems}
        </Card.Body>
      </Card>
    </Col>
  );
}

const getCellContent = (dayName, i) => {
  if (i == 0) {
    return dayName;
  } else if (dayName == "Sunday" && (i - 1) % 3 == 0) {
    return i - 1;
  }
  return '';
};