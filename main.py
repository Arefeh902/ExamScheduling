from models import Course, Student, TimeSlot, Schedule

courses: list[Course]
time_slots: list[TimeSlot]
students: list[Student]
# load exams and time slots

# create GeneticAlgorithm class and call genetic_algorithm

# print results


# import random
# from test_case import test_time_slots
#
# courses = ['math', 'physics', 'bio', 'chem', 'oil', 'cs', 'religion', 'literature']
#
#
# def generate_random_solution() -> Schedule:
#     schedule: Schedule = Schedule(test_time_slots)
#     for course in courses:
#         slot: TimeSlot = random.choice(test_time_slots)
#         schedule.time_to_course[slot].append(course)
#         schedule.course_to_time[course] = slot
#     return schedule
#
# tmp = generate_random_solution()
# for x in tmp.time_to_course:
#     print(x, tmp.time_to_course[x])
#
# for x in tmp.course_to_time:
#     print(x, tmp.course_to_time[x])
