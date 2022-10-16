from typing import List
from flask import Flask, request
from flask_cors import CORS
import sys

from task import Task, task_factory
from task_scheduler import schedule_tasks

app = Flask(__name__)
CORS(app)

@app.route('/send_tasks', methods=['POST'])
def generate_schedules() -> List[Task]:
    print('ELLO', file=sys.stdout, flush=True)
    print('asfdasdf', file=sys.stdout, flush=True)
    r = request.get_json(force=True)
    print(r, file=sys.stdout, flush=True)

    tasks_list = task_factory(r['tasks'], r['zip'])
    schedule = schedule_tasks(tasks_list)

    response = {'result': [
        task.to_json() for task in schedule
    ]}

    print(response  )

    return response