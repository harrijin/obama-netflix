import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import DayColumn from "./DayColumn"
import TaskSidebar from "./TaskSidebar";
import { useState } from "react";

function App() {
  const [schedule, setSchedule] = useState(null);
  return (
    <div className="App">
      <Container style={{margin: 0, height: '100vh'}}>
        <Row style={{width: '100vw', height: '100%'}}>
          <Col xs={3} style={{height: '100%'}}>
            <TaskSidebar handleScheduleUpdate={(result) => {
              setSchedule(result);
              console.log(result);
              console.log(result.result);
            }}/>
          </Col>
          <DayColumn tasks={schedule ? schedule.result : null} dayIndex={0} dayName='Sunday'/>
          <DayColumn tasks={schedule ? schedule.result : null} dayIndex={1} dayName='Monday'/>
          <DayColumn tasks={schedule ? schedule.result : null} dayIndex={2} dayName='Tuesday'/>
          <DayColumn tasks={schedule ? schedule.result : null} dayIndex={3} dayName='Wednesday'/>
          <DayColumn tasks={schedule ? schedule.result : null} dayIndex={4} dayName='Thursday'/>
          <DayColumn tasks={schedule ? schedule.result : null} dayIndex={5} dayName='Friday'/>
          <DayColumn tasks={schedule ? schedule.result : null} dayIndex={6} dayName='Saturday'/>

        </Row>
      </Container>
    </div>
  );
}

export default App;
