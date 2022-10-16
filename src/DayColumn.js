import "./DayColumn.css";
import Card from "react-bootstrap/Card";
import { Col, Table } from "react-bootstrap";
import { useState } from "react";

export default function DayColumn({ dayName }) {
  const [tasks, setTasks] = useState([
    { name: "Task 1", time: 540, duration: 60 },
    { name: "Task 2", time: 1020, duration: 90 },
  ]);

  const ROUND = 3;
  const hours = [];
  const taskElems = tasks.map((task, i) => {
    const chunk = (window.innerHeight - ROUND * 2) / 25;
    const h = (task.duration / 60) * chunk;
    const y = (task.time / 60 + 1) * chunk;

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
  });

  for (let i = 0; i < 25; i++) {
    const h = (window.innerHeight - ROUND * 2) / 25;

    hours.push(
      <div
        key={i}
        style={{
          height: h,
          backgroundColor: i == 0 ? "transparent" : "lightblue",
          borderBottom: i == 24 ? "0px" : "1px solid white",
        }}
      >
        {i == 0 ? dayName : ""}
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
