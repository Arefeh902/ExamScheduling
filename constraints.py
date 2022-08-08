from models import Course, Student, TimeSlot, Schedule
from models import SLOT_PER_DAY


# Helper functions
def get_student_time_slots(schedule: Schedule, student: Student) -> list[int]:
    times: list[int] = []
    for course in student.courses:
        times.append(schedule.course_to_time[course].pk)
    times.sort()
    return times


# Hard Constraints
def student_has_two_exams_in_one_day(schedule: Schedule, student: Student) -> bool:
    times: list[int] = get_student_time_slots(schedule, student)
    for i in range(1, len(times)):
        if times[i]//SLOT_PER_DAY == times[i-1]//SLOT_PER_DAY:
            return True
    return False


def professor_has_tow_exams_in_one_slot(schedule: Schedule, professor: str) -> bool:
    times: list[int] = []
    for course in schedule.course_to_time:
        if course.professor == professor:
            times.append(schedule.course_to_time[course].pk)
    times.sort()
    for i in range(1, len(times)):
        if times[i] == times[i-1]:
            return True
    return False


# Soft Constraints
def has_two_consecutive_exams(schedule: Schedule, student: Student) -> int:
    times: list[int] = get_student_time_slots(schedule, student)
    count: int = 0
    for i in range(1, len(times)):
        if times[i]//SLOT_PER_DAY == times[i-1]//SLOT_PER_DAY + 1:
            count += 1
    return count


def has_three_consecutive_exams(schedule: Schedule, student: Student) -> int:
    times: list[int] = get_student_time_slots(schedule, student)
    count: int = 0
    for i in range(2, len(times)):
        if times[i-2]//SLOT_PER_DAY == times[i-1]//SLOT_PER_DAY - 1 == times[i]//SLOT_PER_DAY - 2:
            count += 1
    return count


def has_exam_on_holidays(schedule: Schedule, student: Student) -> int:
    count: int = 0
    for course in student.courses:
        if schedule.course_to_time[course].is_holiday:
            count += 1
    return count


def calculate_penalty_of_student(schedule: Schedule, student: Student) -> int:
    penalty: int = 0

    penalty += 1000 * has_two_consecutive_exams(schedule, student)
    penalty += 50000 * has_three_consecutive_exams(schedule, student)
    penalty += 10 * has_exam_on_holidays(schedule, student)

    return penalty
