from models import SLOT_PER_DAY, Schedule, Student
from utils import get_student_time_slots


def student_has_two_exams_in_one_day(schedule: Schedule, student: Student) -> bool:
    times: list[int] = get_student_time_slots(schedule, student)
    for i in range(1, len(times)):
        if times[i] // SLOT_PER_DAY == times[i-1] // SLOT_PER_DAY:
            return True
    return False


def professor_has_tow_exams_in_one_slot(schedule: Schedule, professor: str) -> bool:
    times: list[int] = []
    for course in schedule.get_courses():
        if course.professor == professor:
            times.append(schedule.get_course_time(course).pk)

    times.sort()

    for i in range(1, len(times)):
        if times[i] == times[i-1]:
            return True
    return False

def validate_hard_constraints(schedule: Schedule, algorithm_instance) -> bool :

    for student in algorithm_instance.students:
        if student_has_two_exams_in_one_day(schedule, student):
            return False
            
    for prof in algorithm_instance.professors:
        if professor_has_tow_exams_in_one_slot(schedule, prof):
            return False

    return True