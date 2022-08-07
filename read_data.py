from models import Course, Student, TimeSlot, Schedule
import csv

time_slots: list[TimeSlot] = []
professors: list[str] = []


def read_student_and_course_data(path_to_file: str) -> tuple[list[Course], list[Student]]:
    courses: list[Course] = []
    students: list[Student] = []

    file = open(path_to_file)
    csv_reader = csv.reader(file)

    courses_names = next(csv_reader)
    for name in courses_names[2:]:
        courses.append(Course(name, '', []))

    for row in csv_reader:
        student_id: int = int(row[1])
        student: Student = Student(student_id, [])
        for i in range(2, len(row)):
            if row[i] != '':
                student.courses.append(courses[i-2])
                courses[i-2].students_ids.append(student_id)
        students.append(student)

    # for course in courses:
    #     print(course.title, course.students_ids)
    # for student in students:
    #     print(student.pk, student.courses)

    return courses, students


