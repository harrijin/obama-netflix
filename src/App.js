import "./App.css";
import "bootstrap/dist/css/bootstrap.min.css";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import DayColumn from "./DayColumn"
import TaskSidebar from "./TaskSidebar";

function App() {
  return (
    <div className="App">
      <Container style={{margin: 0, height: '100vh'}}>
        <Row style={{width: '100vw', height: '100%'}}>
          <Col xs={3} style={{height: '100%'}}>
            <TaskSidebar />
          </Col>
          <DayColumn dayName='Sunday'/>
          <DayColumn dayName='Monday'/>
          <DayColumn dayName='Tuesday'/>
          <DayColumn dayName='Wednesday'/>
          <DayColumn dayName='Thursday'/>
          <DayColumn dayName='Friday'/>
          <DayColumn dayName='Saturday'/>

        </Row>
      </Container>
    </div>
  );
}

export default App;
