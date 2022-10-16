import json
import datetime
from typing import Any, Dict, List, Tuple

from weather import WeatherCondition, WeatherForecast

class Task:
    name: str
    description: str
    task_id: int # lol
    duration: datetime.timedelta
    prerequisites: List[int] # List of task_ids
    # Allowlist of times + days this task can be done
    allowed_times: Dict[int, List[Tuple[datetime.time, datetime.time]]] # {day: [(start_time, end_time)]}
    scheduled_time: Tuple[int, datetime.time, int, datetime.time] # (day_of_week, start, day_of_week, end) (0 == Sunday)
    
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
                Key: day, 0 == Sunday
                Value: List of time intervals (start_time, end_time)
        """
        self.name = name
        self.description = description
        self.task_id = task_id
        self.duration = duration
        self.prerequisites = prerequisites
        self.allowed_times = allowed_times

    def to_json(self):
        start_time = self.scheduled_time[1]
        start_timedelta = datetime.timedelta(hours=start_time.hour, minutes=start_time.minute, seconds=start_time.second)
        return {
            "name" : self.name,
            "description" : self.description,
            "task_id" : self.task_id,
            "duration" : int(self.duration.total_seconds()/60),
            "start_time" : (self.scheduled_time[0], int(start_timedelta.total_seconds()/60)),
        }

        
def modify_allowed_times(
    allowed_days: List[int],
    allowed_times: Tuple[datetime.time, datetime.time],
    allowed_weather: List[WeatherCondition],
    zip_code: str,
) -> Dict[int, List[Tuple[datetime.time, datetime.time]]]:
    """Modifies the allowed times to account for weather

    Args:
        allowed_days (List[int]): allowed days
        allowed_times (Tuple[datetime.time, datetime.time]): (start_time, end_time)
        allowed_weather (List[WeatherCondition]): allowed weather conditions
        zip_code (str): zip code

    Returns:
        Dict[int, List[Tuple[datetime.time, datetime.time]]]: 
    """
    # if everything in weather constraints is True (i.e. no weather constraints), just return it without querying weather API
    if len(allowed_weather) == 5:
        return {
            i: [allowed_times] for i in range(7)
        }
    res = {
        j: [] for j in range(7)
    }
    forecast = WeatherForecast(zip_code)
    start_time = allowed_times[0]
    end_time = allowed_times[1]
    one_hour = datetime.timedelta(hours=1)
    for day in allowed_days:
        # Check weather in provided time interval
        l = start_time
        while l < end_time:
            r = l + one_hour
            while (r < end_time) and (forecast.check_weather(r) in allowed_weather):
                r += one_hour
            res[day].append((l, r))
            while (l < end_time) and (forecast.check_weather(l) not in allowed_weather):
                l += one_hour
    return res

def task_factory(form_data: List[Dict[str, Any]], zip_code: str) -> List[Task]:
    res = []
    for i in range(len(form_data)):
        task_data = form_data[i]
        allowed_days = [j for j in range(len(task_data['dayConstraints'])) if task_data['dayConstraints'][j]]
        if not task_data['timeConstraints'][0]:
            start_time = 0
            end_time = 24*60 - 1
        else:
            start_time = task_data['timeConstraints'][0] # minutes past midnight
            end_time = task_data['timeConstraints'][1] # minutes past midnight
        allowed_times = (
            datetime.time(
                hour=(start_time // 60),
                minute=(start_time % 60)
            ),
            datetime.time(
                hour=(end_time // 60),
                minute=(end_time % 60)
            )
        )
        weather_constraints = {
            # Sunny
            # Rainy
            # Cloudy
            # Fog
            # Snow
            WeatherCondition.SUNNY: task_data['weather'][0],
            WeatherCondition.RAIN: task_data['weather'][1],
            WeatherCondition.CLOUDY: task_data['weather'][2],
            WeatherCondition.FOG: task_data['weather'][3],
            WeatherCondition.SNOW: task_data['weather'][4],
        }
        allowed_weather = [weather_cond for weather_cond, allowed in weather_constraints.items() if allowed]
        modified_allowed_times = modify_allowed_times(
            allowed_days,
            allowed_times,
            allowed_weather,
            zip_code
        )
        duration = datetime.timedelta(minutes=task_data['duration'])
        res.append(
            Task(
                name=task_data['name'],
                description=task_data['description'],
                task_id=i,
                duration=duration,
                prerequisites=[],
                allowed_times=modified_allowed_times,
            )
        )
    return res
