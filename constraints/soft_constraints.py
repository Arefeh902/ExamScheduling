from models import TimeSlot, Student, Schedule
from utils import get_student_time_slots


def calculate_number_of_two_consecutive_exams(schedule: Schedule, student: Student) -> int:
    times: list[TimeSlot] = get_student_time_slots(schedule, student)
    count: int = 0

    for i in range(1, len(times)):
        if times[i-1].get_day() == times[i].get_day() - 1:
            count += 1

    return count


def calculate_number_of_three_consecutive_exams(schedule: Schedule, student: Student) -> int:
    times: list[TimeSlot] = get_student_time_slots(schedule, student)
    count: int = 0

    for i in range(2, len(times)):
        if times[i-2].get_day() == times[i-1].get_day() - 1 == times[i].get_day() - 2:
            count += 1

    return count


def calculate_number_of_exams_on_holidays(schedule: Schedule, student: Student) -> int:
    count: int = 0

    for course_id in student.courses:
        if schedule.get_course_time_by_id(course_id).is_holiday:
            count += 1

    return count


def calculate_number_of_single_day_rest(schedule: Schedule, student: Student) -> int :
    times: list[TimeSlot] = get_student_time_slots(schedule, student)
    count: int = 0

    for i in range(1, len(times)):
        if times[i-1].get_day() == times[i].get_day() - 2:
            count += 1

    return count


def calculate_number_of_two_consecutive_days_rest(schedule: Schedule, student: Student) -> int :
    times: list[TimeSlot] = get_student_time_slots(schedule, student)
    count: int = 0

    for i in range(1, len(times)):
        if times[i - 1].get_day() == times[i].get_day() - 3:
            count += 1

    return count


class Penalty:
    TWO_CONSECUTIVE_EXAM = 1000
    THREE_CONSECUTIVE_EXAM = 50000
    EXAM_ON_HOLIDAY = 1000
    SINGLE_DAY_REST = 500
    TWO_CONSECUTIVE_DAYS_REST = 250
    

def calculate_penalty_of_student(schedule: Schedule, student: Student) -> int:
    penalty: int = 0

    penalty += Penalty.TWO_CONSECUTIVE_EXAM * calculate_number_of_two_consecutive_exams(schedule, student)
    penalty += Penalty.THREE_CONSECUTIVE_EXAM * calculate_number_of_three_consecutive_exams(schedule, student)
    penalty += Penalty.EXAM_ON_HOLIDAY * calculate_number_of_exams_on_holidays(schedule, student)
    penalty += Penalty.SINGLE_DAY_REST * calculate_number_of_single_day_rest(schedule, student)
    penalty += Penalty.TWO_CONSECUTIVE_DAYS_REST * calculate_number_of_two_consecutive_days_rest(schedule, student)

    return penalty
