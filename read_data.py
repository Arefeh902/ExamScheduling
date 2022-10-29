from models import Course, Student, TimeSlot
import csv


def read_courses_data(courses) -> list[Course]:
    courses_list: list[Course] = []
    for course in courses:
        courses_list.append(Course(course["pk"], course["title"], "", [], course["is_first"]))
    return courses_list


def read_students_data(students, courses) -> list[Student]:
    students_list: list[students] = []
    for student in students:
        students_list.append(Student(student["pk"], student["courses"]))
        for course_id in student["courses"]:
            course: Course = Course.get_course_by_id(courses, course_id)
            course.students_ids.append(student["pk"])
    return students_list


def read_professors_data(professors, courses) -> list[str]:
    professors_list: list[str] = []
    for prof in professors:
        prof_name = prof["name"]
        professors_list.append(prof_name)
        for course_id in prof["courses"]:
            course: Course = Course.get_course_by_id(courses, course_id)
            course.professor = prof_name
    return professors_list


def read_time_slots_data(time_slots) -> list[TimeSlot]:
    time_slots_list: list[TimeSlot] = []
    for slot in time_slots:
        time_slots_list.append(TimeSlot(slot["pk"], slot["is_available"], slot["is_holiday"], slot[""]))
    return time_slots_list

