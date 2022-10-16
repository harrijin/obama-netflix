import Accordion from "react-bootstrap/Accordion";
import Card from "react-bootstrap/Card";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import InputGroup from "react-bootstrap/InputGroup";
import Dropdown from "react-bootstrap/Dropdown";

import { useState } from "react";

export default function TaskSidebar({handleScheduleUpdate}) {
  const [tasks, setTasks] = useState([]);

  const [isShowingForm, setShowingForm] = useState(false);

  const [formInput, setFormInput] = useState({
    name: "",
    duration: 0,
    description: "",
    weather: [true, true, true, true, true],
    dayConstraints: [true, true, true, true, true, true, true],
    timeConstraints: [null, null],
  });

  const weathers = ["Sunny", "Rain", "Cloudy", "Fog", "Snow"];
  const days = [
    "Sunday",
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
  ];

  const [zip, setZip] = useState("");

  const handleSubmit = async () => {
    const payload = {zip: zip, tasks: tasks}
    console.log(JSON.stringify(payload));
    const response = await fetch(
      "http://localhost:5000/send_tasks",
      {
        method: "POST",
        headers: {
          Accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
        mode: 'cors'
      }
    );
    response.json().then((result) => {
      console.log(result);
      handleScheduleUpdate(result);
    })
  }

  return (
    <Card body style={{ height: "100%" }}>
      {!isShowingForm && (
        <>
          {tasks.map((task, i) => (
            <Accordion key={i}>
              <Accordion.Item eventKey={i}>
                <Accordion.Header>{task.name}</Accordion.Header>
                <Accordion.Body>
                  <i>{task.duration + " hours"}</i>
                  <br />
                  {task.description}
                </Accordion.Body>
              </Accordion.Item>
            </Accordion>
          ))}

          <Button
            style={{ marginTop: 20 }}
            onClick={() => setShowingForm(true)}
          >
            Add Task
          </Button>
          <br />
          <Form style={{ marginTop: 10 }}>
            <Form.Group className="mb-3" controlId="zip">
              <b>
                <Form.Label required>Zip</Form.Label>
              </b>
              <Form.Control
                onChange={(e) => setZip(e.target.value)}
                required
                type="text"
                placeholder="Enter zip code for weather"
                value={zip}
              />
            </Form.Group>
          </Form>
          <br />
          <Button
            style={{ marginTop: 20 }}
            disabled={
              tasks.length <= 0 || !zip || zip.trim() == "" || zip.length < 5
            }
            onClick={() => handleSubmit()}
          >
            Generate Schedule
          </Button>
        </>
      )}
      {isShowingForm && (
        <Form>
          <Form.Group className="mb-3" controlId="name">
            <b>
              <Form.Label required>Name</Form.Label>
            </b>
            <Form.Control
              onChange={(e) =>
                setFormInput({ ...formInput, name: e.target.value })
              }
              required
              type="text"
              placeholder="Enter name of task"
            />
          </Form.Group>
          <Form.Group className="mb-3" controlId="duration">
            <b>
              <Form.Label required>Duration (hours)</Form.Label>
            </b>
            <Form.Control
              onChange={(e) =>
                setFormInput({ ...formInput, duration: Number(e.target.value) * 60 })
              }
              required
              type="number"
              step="0.5"
              placeholder="Enter duration"
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="description">
            <b>
              <Form.Label>Description</Form.Label>
            </b>
            <Form.Control
              as="textarea"
              rows={3}
              onChange={(e) =>
                setFormInput({ ...formInput, description: e.target.value })
              }
            />
          </Form.Group>

          <Form.Group className="mb-3" controlId="weatherConstraints">
            <b>
              <Form.Label>Weather Allowed</Form.Label>
            </b>

            <Dropdown>
              <Dropdown.Toggle variant="secondary">Select</Dropdown.Toggle>

              <Dropdown.Menu>
                <div style={{ padding: 10 }}>
                  {weathers.map((w, i) => (
                    <Form.Check
                      key={i}
                      type="checkbox"
                      label={w}
                      checked={formInput.weather[i]}
                      onChange={() => {
                        let newConstraints = formInput.weather;
                        newConstraints[i] = !newConstraints[i];
                        setFormInput({
                          ...formInput,
                          weather: newConstraints,
                        });

                        console.log(formInput);
                      }}
                    />
                  ))}
                </div>
              </Dropdown.Menu>
            </Dropdown>
          </Form.Group>

          <Form.Group className="mb-3" controlId="dayConstraints">
            <b>
              <Form.Label>Day of Week Constraint</Form.Label>
            </b>
            <Dropdown>
              <Dropdown.Toggle variant="secondary">Select</Dropdown.Toggle>

              <Dropdown.Menu>
                <div style={{ padding: 10 }}>
                  {days.map((d, i) => (
                    <Form.Check
                      key={i}
                      type="checkbox"
                      label={d}
                      checked={formInput.dayConstraints[i]}
                      onChange={() => {
                        let newConstraints = formInput.dayConstraints;
                        newConstraints[i] = !newConstraints[i];
                        setFormInput({
                          ...formInput,
                          dayConstraints: newConstraints,
                        });
                      }}
                    />
                  ))}{" "}
                </div>
              </Dropdown.Menu>
            </Dropdown>
          </Form.Group>

          <Form.Group className="mb-3" controlId="timeConstraint">
            <b>
              <Form.Label required>Time Constraint</Form.Label>
            </b>
            <InputGroup className="mb-3">
              <InputGroup.Text style={{ width: "25%" }}>Start</InputGroup.Text>
              <Form.Control
                type="time"
                onChange={(e) => {
                  const timeString = e.target.value.split(":");
                  const minutes = +timeString[0] * 60 + +timeString[1];
                  const updated = formInput.timeConstraints;
                  updated[0] = minutes;
                  setFormInput({
                    ...formInput,
                    timeConstraints: updated,
                  });
                }}
              />
            </InputGroup>

            <InputGroup className="mb-3">
              <InputGroup.Text style={{ width: "25%" }}>End</InputGroup.Text>
              <Form.Control
                type="time"
                onChange={(e) => {
                  const timeString = e.target.value.split(":");
                  const minutes = +timeString[0] * 60 + +timeString[1];
                  const updated = formInput.timeConstraints;
                  updated[1] = minutes;
                  setFormInput({
                    ...formInput,
                    timeConstraints: updated,
                  });
                }}
              />
            </InputGroup>
          </Form.Group>

          <Form.Group className="mb-3" controlId="prereqs">
            <b>
              <Form.Label>Prerequisites</Form.Label>
            </b>
            <Form.Select aria-label="Default select">
              <option>(none)</option>
              {tasks.map((task, i) => (
                <option key={i}> {task.name}</option>
              ))}
            </Form.Select>
          </Form.Group>

          <Button
            variant="primary"
            onClick={() => {
              setTasks([...tasks, formInput]);
              setFormInput({
                name: "",
                duration: 0,
                description: "",
                weather: [true, true, true, true, true],
                dayConstraints: [true, true, true, true, true, true, true],
                timeConstraints: [null, null],
              });
              setShowingForm(false);
              console.log(tasks);
            }}
            disabled={
              !formInput.name ||
              formInput.name === "" ||
              !formInput.duration ||
              formInput.duration <= 0
            }
          >
            Submit
          </Button>
        </Form>
      )}
    </Card>
  );
}
