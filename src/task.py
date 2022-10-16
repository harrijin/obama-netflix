import datetime
from typing import Any, Dict, List, Tuple

from weather import WeatherCondition

class Task:
    name: str
    description: str
    task_id: int # lol
    duration: datetime.timedelta
    prerequisites: List[int] # List of task_ids
    # Allowlist of times + days this task can be done
    allowed_times: Dict[int, List[Tuple[datetime.time, datetime.time]]] # {day: [(start_time, end_time)]}
    
    def __init__(
        self,
        name: str,
        description: str,
        task_id: int,
        duration: datetime.timedelta,
        prerequisites: List[int],
        allowed_times: Dict[int, List[Tuple[datetime.time, datetime.time]]],
    ):
        """Constructor for a Task object

        Args:
            name (str): Name of the task (does not have to be unique)
            description (str): Description of the task
            task_id (int): Unique task id
            duration (datetime.timedelta): Duration of the task
            prequisites (List[int]): List of task IDs that should be completed prior to this task being executed
            allowed_times (Dict[int, List[Tuple[datetime.time, datetime.time]]]): 
                Key: day, 0 == Monday
                Value: List of time intervals (start_time, end_time)
        """
        self.name = name
        self.description = description
        self.task_id = task_id
        self.duration = duration
        self.prerequisites = prerequisites
        self.allowed_times = allowed_times
        
def modify_allowed_times(
    allowed_days: List[int],
    allowed_times: Tuple[datetime.time, datetime.time],
    weather_constraints: Dict[WeatherCondition, bool],
    zip_code: str,
) -> Dict[int, List[Tuple[datetime.time, datetime.time]]]:
    """Modifies the allowed times to account for weather

    Args:
        allowed_days (List[int]): _description_
        allowed_times (Tuple[datetime.time, datetime.time]): (start_time, end_time)
        weather_constraints (Dict[WeatherCondition, bool]): value is true if the task can be performed in this weather condition
        zip_code (str): zip code

    Returns:
        Dict[int, List[Tuple[datetime.time, datetime.time]]]: 
    """
    # if everything in weather constraints is True (i.e. no weather constraints), just return it without querying weather API
    if all(allowed_days.values()):
        return {
            i: allowed_times for i in range(7)
        }
    res = {}
    for day in allowed_days:
        # Check weather in provided time interval
        pass
    return res

def task_factory(form_data: List[Dict[str, Any]], zip_code: str) -> List[Task]:
    res = []
    for i in range(len(form_data)):
        task_data = form_data[i]
        allowed_days = [j for j in range(len(task_data['Allowed Days'])) if task_data['Allowed Days'][j]]
        allowed_times = (datetime.time(task_data['Start Time']), datetime.time(task_data['End Time']))
        weather_constraints = {
            WeatherCondition.SUNNY: task_data['Weather Constraints']['Sunny'],
            WeatherCondition.CLOUDY: task_data['Weather Constraints']['Cloudy'],
            WeatherCondition.FOG: task_data['Weather Constraints']['Fog'],
            WeatherCondition.RAIN: task_data['Weather Constraints']['Rain'],
            WeatherCondition.SNOW: task_data['Weather Constraints']['Snow'],
        }
        
        modified_allowed_times = modify_allowed_times(
            allowed_days,
            allowed_times,
            weather_constraints,
            zip_code
        )
        res.append(
            Task(
                name=task_data['Task Name'],
                task_id=i,
                duration=task_data['Duration'],
                prerequisites=task_data['Prerequisites'],
                allowed_times=modified_allowed_times,
            )
        )
    return res
