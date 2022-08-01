from models import Course, TimeSlot, Schedule

courses: list[Course]
time_slots: list[TimeSlot]

# load exams and time slots

# create GeneticAlgorithm class and call genetic_algorithm

# print results


# import random
# from test_case import test_time_slots
#
# courses = ['math', 'physics', 'bio', 'chem', 'naft', 'cs', 'elah']
#
# def generate_random_solution() -> Schedule:
#     schedule: Schedule = Schedule(test_time_slots)
#     for course in courses:
#         slot: TimeSlot = random.choice(test_time_slots)
#         schedule.mapping[slot].append(course)
#     return schedule
#
# tmp = generate_random_solution()
# for x in tmp.mapping:
#     print(x, tmp.mapping[x])
