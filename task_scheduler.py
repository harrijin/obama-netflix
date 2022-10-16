
import datetime as dt
# import secrets
# from multiprocessing.reduction import duplicate
# import sched

tasks1 = [('A', 60, {'Tue': [(dt.time(1), dt.time(3))]}),  # A 1hr Wed 1-2
          #  ('B', 90, {'Thu': [(dt.time(1, 30), dt.time(3))]}),
          ('C', 30, {'Tue': [(dt.time(2, 30), dt.time(3))]})]

tasks2 = [('A', 60, {'Tue': [(dt.time(1), dt.time(6))]}),  # A 1hr Wed 1-2
          #  ('B', 90, {'Thu': [(dt.time(1, 30), dt.time(3))]}),
          ('C', 30, {'Tue': [(dt.time(2, 30), dt.time(3))]})]

tasks = tasks1
tasks = tasks2


class time_slot:
    def __init__(self, start, end, task):
        self.start = start
        self.end = end
        self.task = task  # string


time_slots = []  # all tasks’ time slots

weekday_offset_dict = {'Sun': 0,
                       'Mon': 1,
                       'Tue': 2,
                       'Wed': 3,
                       'Thu': 4,
                       'Fri': 5,
                       'Sat': 6}

# loop thru tasks, create time_slots


def get_time_slots(tasks1):
    time_slots = []
    for task_tuple in tasks1:
        task_name = task_tuple[0]
        task_duration = task_tuple[1]
        task_weekday_dict = task_tuple[2]
        # print('\ntask_name:', task_name)
        # print('task_duration:', task_duration)
        # print('task_weekday_dict:', task_weekday_dict)

        # weekdays and their time intervals
        for day, day_intervals_array in task_weekday_dict.items():
            # all task intervals for the day
            # print('day:', day)
            # print('day_intervals_array:', day_intervals_array)
            for task_endpts in day_intervals_array:
                weekday_offset = 24 * 60 * weekday_offset_dict[day]
                start_military = task_endpts[0].hour * \
                    60 + task_endpts[0].minute
                end_military = task_endpts[1].hour * 60 + task_endpts[1].minute
                task_start = start_military + weekday_offset
                task_end = end_military + weekday_offset
                # print("stuff", task_start, task_end, task_duration)
                # add all potential task durations
                for start in range(task_start, task_end-task_duration+30, 30):
                    time_slots.append(
                        time_slot(start, start+task_duration, task_name))
                    # print('appended')
    return time_slots


time_slots = get_time_slots(tasks)
# sort time slots


time_slots = sorted(time_slots, key=lambda x: (x.end, x.start))

print('all blocks')
for slot in time_slots:
    print(slot.task, ': ', slot.start, '-', slot.end)

# def sort_function:
#     # TODO

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


task_counts = interval_schedule(time_slots)

print('task_counts', task_counts, '\n')

# print('scheduled blocks:')
# for task in scheduled_tasks:
#     print(task.task, task.start, '-', task.end)
# print()


def print_scheduled(tasks):
    print('scheduled blocks:')
    for task in tasks:
        print(task.task, task.start, '-', task.end)


unscheduled_tasks = tasks
for task in tasks:
    task_name = task[0]
    if task_name in task_counts:
        unscheduled_tasks.remove(task)

print('unscheduled_tasks:', unscheduled_tasks)


duplicate_tasks = []
for task_name, count in task_counts.items():
    if count > 1:
        for task in scheduled_tasks:
            if task.task == task_name:
                duplicate_tasks.append(task)

# print('duplicate_tasks', duplicate_tasks)
# print('my dup')
# print_scheduled(duplicate_tasks)


def no_duplicates(task_counts):
    for task_name, counts in task_counts.items():
        if counts > 1:
            return True

    return False


# print('no_duplicates', no_duplicates(task_counts))

unscheduled_tasks_slots = get_time_slots(unscheduled_tasks)

second_break = False
final_task_reached = False
one_pass = True
while one_pass:
    one_pass = False
    # print('oh no dup', task_counts)
    for dupe_task in duplicate_tasks:
        for unscheduled_block in unscheduled_tasks_slots:
            if unscheduled_block.start >= dupe_task.start and unscheduled_block.end <= dupe_task.end:

                scheduled_tasks.remove(dupe_task)
                task_counts[dupe_task.task] -= 1
                scheduled_tasks.append(unscheduled_block)
                task_counts[unscheduled_block.task] = 1
                # print('break')
                break
            if dupe_task == duplicate_tasks[-1]:
                final_task_reached = True

# print_scheduled(duplicate_tasks)

remove_tasks = []
for task in scheduled_tasks:
    if task_counts[task.task] > 1:
        remove_tasks.append(task)
        task_counts[task.task] -= 1
# print_scheduled(remove_tasks)

for rm_task in remove_tasks:
    scheduled_tasks.remove(rm_task)


print('scheduled blocks:')
for task in scheduled_tasks:
    print(task.task, task.start, '-', task.end)
print()
# print(task_counts)

# times_slots = sorted(times_slots, key=itemgetter('end', 'start'))

# interval scheduling
