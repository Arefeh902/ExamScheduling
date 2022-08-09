from models import Student, Schedule
from models import SLOT_PER_DAY
from utils import get_student_time_slots


def calculate_number_of_two_consecutive_exams(schedule: Schedule, student: Student) -> int:
    times: list[int] = get_student_time_slots(schedule, student)
    count: int = 0

    for i in range(1, len(times)):
        if times[i] // SLOT_PER_DAY == times[i-1] // SLOT_PER_DAY + 1:
            count += 1

    return count


def calculate_number_of_three_consecutive_exams(schedule: Schedule, student: Student) -> int:
    times: list[int] = get_student_time_slots(schedule, student)
    count: int = 0

    for i in range(2, len(times)):
        if times[i-2] // SLOT_PER_DAY == times[i-1] // SLOT_PER_DAY - 1 == times[i] // SLOT_PER_DAY - 2:
            count += 1

    return count


def calculate_number_of_exams_on_holidays(schedule: Schedule, student: Student) -> int:
    count: int = 0

    for course in student.courses:
        if schedule.get_course_time(course).is_holiday:
            count += 1

    return count


class Penalty:
    TWO_CONSECUTIVE_EXAM = 1000
    THREE_CONSECUTIVE_EXAM = 50000
    EXAM_ON_HOLIDAY = 10

def calculate_penalty_of_student(schedule: Schedule, student: Student) -> int:
    penalty: int = 0

    penalty += Penalty.TWO_CONSECUTIVE_EXAM * calculate_number_of_two_consecutive_exams(schedule, student)
    penalty += Penalty.THREE_CONSECUTIVE_EXAM * calculate_number_of_three_consecutive_exams(schedule, student)
    penalty += Penalty.EXAM_ON_HOLIDAY * calculate_number_of_exams_on_holidays(schedule, student)

    return penalty