from models import TimeSlot, Student, Schedule
from utils import get_student_time_slots
from constraints.hard_constraints import calculate_exams_in_one_day


def calculate_number_of_two_consecutive_exams(schedule: Schedule, student: Student) -> int:
    times: list[TimeSlot] = get_student_time_slots(schedule, student)
    count: int = 0

    for i in range(0, len(times) - 1):
        for j in range(i+1, len(times) - 1):
            if times[j].get_day() - times[i].get_day() > 1:
                break
            if times[i].get_day() == times[j].get_day() - 1:
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


def calculate_number_of_single_day_rest(schedule: Schedule, student: Student) -> int:
    times: list[TimeSlot] = get_student_time_slots(schedule, student)
    count: int = 0

    for i in range(0, len(times) - 1):
        for j in range(i+1, len(times)):
            if times[j].get_day() - times[i].get_day() > 2:
                break
            if times[i].get_day() == times[j].get_day() - 2:
                count += 1

    return count


def calculate_number_of_two_consecutive_days_rest(schedule: Schedule, student: Student) -> int:
    times: list[TimeSlot] = get_student_time_slots(schedule, student)
    count: int = 0

    for i in range(1, len(times)):
        if times[i - 1].get_day() == times[i].get_day() - 3:
            count += 1

    return count


class Penalty:
    TWO_EXAMS_IN_ONE_DAY = 12
    TWO_CONSECUTIVE_EXAM = 3
    THREE_CONSECUTIVE_EXAM = 9
    EXAM_ON_HOLIDAY = 0
    SINGLE_DAY_REST = 0
    # TWO_CONSECUTIVE_DAYS_REST = 0.5
    # COINCIDES_WITH_GENERAL_EXAMS = 1
    

# def calculate_penalty_of_student(schedule: Schedule, student: Student) -> int:
#     penalty: int = 0
#
#     schedule.two_consecutive_exams = calculate_number_of_two_consecutive_exams(schedule, student)
#     schedule.students_with_two_consecutive_exams += 1 if schedule.two_consecutive_exams > 0 else 0
#     penalty += Penalty.TWO_CONSECUTIVE_EXAM * schedule.two_consecutive_exams
#
#     schedule.three_consecutive_exams = calculate_number_of_three_consecutive_exams(schedule, student)
#     schedule.students_with_three_consecutive_exams += 1 if schedule.three_consecutive_exams > 0 else 0
#     penalty += Penalty.THREE_CONSECUTIVE_EXAM * schedule.three_consecutive_exams
#
#     # penalty += Penalty.EXAM_ON_HOLIDAY * calculate_number_of_exams_on_holidays(schedule, student)
#
#     schedule.single_day_rest = calculate_number_of_single_day_rest(schedule, student)
#     schedule.students_with_single_day_rest += 1 if schedule.single_day_rest > 0 else 0
#     penalty += Penalty.SINGLE_DAY_REST * schedule.single_day_rest
#
#     schedule.two_exams_in_one_day = calculate_exams_in_one_day(schedule, student)
#     schedule.students_with_two_exams_in_one_day += 1 if schedule.two_exams_in_one_day > 0 else 0
#     penalty += Penalty.TWO_EXAMS_IN_ONE_DAY * schedule.two_exams_in_one_day
#
#     # penalty += Penalty.TWO_CONSECUTIVE_DAYS_REST * calculate_number_of_two_consecutive_days_rest(schedule, student)
#     return penalty


def calculate_special_and_general_exams_intersection_penalty(schedule: Schedule) -> int:
    ans: int = 0

    for time in schedule.time_to_course:
        for course in schedule.time_to_course[time]:
            if course.is_first_or_second_year_course and time.has_general_exam:
                ans += 1

    return ans * Penalty.COINCIDES_WITH_GENERAL_EXAMS


def calculate_penalty_of_student(schedule: Schedule, student: Student) -> int:
    times: list[TimeSlot] = get_student_time_slots(schedule, student)

    num_of_days: int = 0
    for time in times:
        num_of_days = time.get_day() if num_of_days < time.get_day() else num_of_days

    num_of_days += 1
    days: list = [0] * num_of_days

    for time in times:
        days[time.get_day()] += 1

    two_in_one_day = sum(days)
    two_consecutive = sum([days[i]*days[i+1] for i in range(len(days)-1)])
    three_consecutive = sum([days[i]*days[i+1]*days[i+2] for i in range(len(days)-2)])
    single_day_rest = sum([days[i]*days[i+2] for i in range(len(days)-2)])

    penalty = 0

    schedule.two_exams_in_one_day += two_in_one_day
    schedule.students_with_two_exams_in_one_day += 1 if two_in_one_day > 0 else 0
    penalty += Penalty.TWO_EXAMS_IN_ONE_DAY * two_in_one_day

    schedule.two_consecutive_exams += two_consecutive
    schedule.students_with_two_consecutive_exams += 1 if two_consecutive > 0 else 0
    penalty += Penalty.TWO_CONSECUTIVE_EXAM * two_consecutive

    schedule.three_consecutive_exams += three_consecutive
    schedule.students_with_three_consecutive_exams += 1 if three_consecutive > 0 else 0
    penalty += Penalty.THREE_CONSECUTIVE_EXAM * three_consecutive

    schedule.single_day_rest += single_day_rest
    schedule.students_with_single_day_rest += 1 if single_day_rest > 0 else 0
    penalty += Penalty.SINGLE_DAY_REST * single_day_rest

    return penalty
