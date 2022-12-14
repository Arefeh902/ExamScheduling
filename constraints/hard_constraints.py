from models import Schedule, Student, TimeSlot
from utils import get_student_time_slots


def calculate_exams_in_one_day(schedule: Schedule, student: Student) -> int:
    times: list[TimeSlot] = get_student_time_slots(schedule, student)
    ans: int = 0
    for i in range(1, len(times)):
        if times[i].get_day() == times[i-1].get_day():
            ans += 1
    return ans


def calculate_student_exams_in_one_slot(schedule: Schedule, student: Student) -> int:
    times: list[TimeSlot] = get_student_time_slots(schedule, student)
    ans: int = 0
    for i in range(1, len(times)):
        if times[i] == times[i-1]:
            ans += 1
    return ans


def professor_has_tow_exams_in_one_slot(schedule: Schedule, professor: str) -> bool:
    times: list[TimeSlot] = []
    for course in schedule.get_courses():
        if course.professor == professor:
            times.append(schedule.get_course_time(course))

    times.sort()
    ans: int = 0

    for i in range(1, len(times)):
        if times[i] == times[i-1]:
            ans += 1
    return False


def validate_hard_constraints(schedule: Schedule, algorithm_instance) -> bool:

    for student in algorithm_instance.students:
        if calculate_student_exams_in_one_slot(schedule, student):
            return False
            
    for prof in algorithm_instance.professors:
        if professor_has_tow_exams_in_one_slot(schedule, prof):
            return False

    return True
