import copy
from task import Task
import datetime as dt
import math
# import secrets
# from multiprocessing.reduction import duplicate
# import sched

tasks1 = [
    Task(
        name='A',
        description='dn',
        task_id=0,
        duration=dt.timedelta(minutes=60),
        prerequisites=[],
        allowed_times={
            2: [
                (dt.time(1), dt.time(3))
            ],
            3: [
                (dt.time(1), dt.time(3))
            ],
            4: [
                (dt.time(1), dt.time(3))
            ],
            5: [
                (dt.time(1), dt.time(3))
            ]
        }
    ),
    #  ('B', 90, {'Thu': [(dt.time(1, 30), dt.time(3))]}),
    Task(
        name='C',
        description='dn',
        task_id=1,
        duration=dt.timedelta(minutes=90),
        prerequisites=[],
        allowed_times={
            2: [
                (dt.time(1, 30), dt.time(3))
            ]
        }
    ),
]

# tasks2 = [('A', 60, {'Tue': [(dt.time(1), dt.time(6))]}),  # A 1hr Wed 1-2
#           #  ('B', 90, {'Thu': [(dt.time(1, 30), dt.time(3))]}),
#           ('C', 30, {'Tue': [(dt.time(2, 30), dt.time(3))]})]

tasks = tasks1

def schedule_tasks(tasks):

    class time_slot:
        def __init__(self, start, end, task, t_id):
            self.start = start
            self.end = end
            self.task = task  # string
            # self.index = index
            self.t_id = t_id


    time_slots = []  # all tasks’ time slots

    # loop thru tasks, create time_slots
    def get_time_slots(tasks):
        time_slots = []
        for task_class in tasks:
            task_name = task_class.name
            task_id = task_class.task_id
            # task_index = task_idx
            task_duration = int(task_class.duration.total_seconds()/60)
            task_weekday_dict = task_class.allowed_times

            # weekdays and their time intervals
            for day_idx, day_intervals_array in task_weekday_dict.items():
                # all task intervals for the day
                for task_endpts in day_intervals_array:
                    weekday_offset = 24 * 60 * day_idx
                    start_military = task_endpts[0].hour * \
                        60 + task_endpts[0].minute
                    end_military = task_endpts[1].hour * 60 + task_endpts[1].minute
                    task_start = start_military + weekday_offset
                    task_end = end_military + weekday_offset
                    # add all potential task durations
                    for start in range(task_start, task_end-task_duration+5, 5):
                        time_slots.append(
                            time_slot(start, start+task_duration, task_name, task_id))
        return time_slots


    # sort time slots
    time_slots = get_time_slots(tasks)
    time_slots = sorted(time_slots, key=lambda x: (x.end, x.start))


    def print_scheduled(tasks):
        for task in tasks:
            print(task.task, task.start, '-', task.end)


    # print('all blocks')
    # print_scheduled(time_slots)

    scheduled_tasks = []


    def interval_schedule(time_slots):
        task_counts = {}

        for block in time_slots:
            # add first task
            if len(scheduled_tasks) == 0:
                scheduled_tasks.append(block)
                task_counts[block.task] = 1
            else:
                if block.start >= scheduled_tasks[-1].end:
                    scheduled_tasks.append(block)
                    if block.task in task_counts:
                        # here
                        task_counts[block.task] += 1
                    else:
                        task_counts[block.task] = 1

        return task_counts

    # get counts of scheduled tasks
    task_counts = interval_schedule(time_slots)
    # print('task_counts', task_counts, '\n')
    print(len(scheduled_tasks), 'b')

    # print(task_counts)

    unscheduled_tasks = copy.deepcopy(tasks)
    print('a', len(unscheduled_tasks))

    for task in unscheduled_tasks:
        task_name = task.name
        if task_name in task_counts:
            unscheduled_tasks.remove(task)
    # print('unscheduled_tasks:', unscheduled_tasks)
    print('unsch')
    
    print('b',len(unscheduled_tasks))

    duplicate_tasks = []
    for task_name, count in task_counts.items():
        if count > 1:
            for task in scheduled_tasks:
                if task.task == task_name:
                    duplicate_tasks.append(task)
    
    # TODO: consolidate duplicate tasks by name


    unscheduled_tasks_slots = get_time_slots(unscheduled_tasks)
    print(len(unscheduled_tasks_slots), 'len of un')

    print('dup tasks')
    print_scheduled(duplicate_tasks)
    print('unsched')
    print_scheduled(unscheduled_tasks_slots)
    # first pass - switch in unscheduled tasks
    for dupe_task in duplicate_tasks:
        for unscheduled_block in unscheduled_tasks_slots:
            span = []
            unscheduled_block_duration = unscheduled_block.end - unscheduled_block.start
            dupe_task_duration = dupe_task.end - dupe_task.start
            num_dupe_needed = math.ceil(unscheduled_block_duration / dupe_task_duration)
            
            print('num_dupe_needed', num_dupe_needed)
            num_dupes_found = 1
            dupes_found = [dupe_task]
            print('dupe_task.start', dupe_task.start)
            dupe_start = dupe_task.end
            terminate = True
            print('dupe_start', dupe_start)
            while num_dupes_found < num_dupe_needed:
                for other_dupe in duplicate_tasks:
                    print('other_dupe.start', other_dupe.start)
                    if other_dupe.start == dupe_start:
                        print("went here")
                        num_dupes_found += 1
                        dupe_start = dupe_start + dupe_task_duration
                        dupes_found.append(other_dupe)
                        terminate == False

                    
                if terminate:
                    break

            
            if unscheduled_block.start >= dupe_task.start and num_dupes_found == num_dupe_needed:
                print('b4', len(scheduled_tasks))
                for d in dupes_found:
                    print('remove d ', d.start, d.end)
                    scheduled_tasks.remove(d)
                print('after', len(scheduled_tasks))
                task_counts[dupe_task.task] -= num_dupe_needed
                print(task_counts, 'asdflkajsdfkajsdklfjasf')
                scheduled_tasks.append(unscheduled_block)
                if unscheduled_block.task not in task_counts:
                    task_counts[unscheduled_block.task] = 1
                else:
                    task_counts[unscheduled_block.task] += 1
                print(task_counts, 'asdfsdf')

                break

    print('1st', task_counts)
    # second pass - remove all duplicate tasks
    remove_tasks = []
    scheduled_tasks.reverse()
    for task in scheduled_tasks:
        if task_counts[task.task] > 1:
            remove_tasks.append(task)
            task_counts[task.task] -= 1
    for rm_task in remove_tasks:
        scheduled_tasks.remove(rm_task)

    print(task_counts)
    # print('final scheduled blocks:')
    # print_scheduled(scheduled_tasks)

    # print('len scheudled', len(scheduled_tasks))

    scheduled_tasks.reverse()

    for task in scheduled_tasks:
        task_name = task.task
        military_start = task.start
        military_end = task.end

        start_day = military_start // (24 * 60) 
        end_day = military_end // (24 * 60) 
        
        start_hour = ( military_start % (24 * 60) ) // 60
        start_minute = ( military_start % (24 * 60) ) % 60

        end_hour = ( military_end % (24 * 60) ) // 60
        end_minute = ( military_end % (24 * 60) ) % 60

        task_id = task.t_id

        tasks[task_id].scheduled_time = (start_day, dt.time(start_hour, start_minute), end_day, dt.time(end_hour, end_minute))
        print(task_name)
        print(task_id, tasks[task_id].scheduled_time)

        # print(len(scheduled_tasks))
    # for t in tasks:
    #     print(t.name)
    #     print(t.scheduled_time)
    return tasks

schedule_tasks(tasks)