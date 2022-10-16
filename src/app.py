from typing import List
from flask import Flask, request

from task import Task, task_factory
from task_scheduler import schedule_tasks

app = Flask(__name__)

@app.route('/send_tasks', methods=['POST'])
def generate_schedules() -> List[Task]:
    tasks_list = task_factory(request.form['tasks'], request.form['zip'])
    schedule = schedule_tasks(tasks_list)
    return [
        task.to_json() for task in schedule
    ]