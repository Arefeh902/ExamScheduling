from models import Course, Professor, Student, TimeSlot
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

    file.close()

    return courses, students


def read_professor_data(path_to_file: str) -> list[Professor]:

    lines: list[str] = []
    with open(path_to_file) as file:
        lines = file.readlines()

    # data format:
    # professor_name, course1, course2...

    professors: list[Professor] = []

    for i in range(len(lines)):
        line = lines[i]

        _list = line.split(",")
        professor_name, courses_list = _list[0], _list[1:]

        course_models = [Course(name, professor_name, []) for name in courses_list]

        professors.append(Professor(i+1, professor_name, course_models))
    
    return professors