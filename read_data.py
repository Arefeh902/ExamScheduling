from models import Course, Student
import csv


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


def read_professor_data(path_to_file: str, all_courses: list[Course]) -> list[str]:

    lines: list[str] = []
    with open(path_to_file) as file:
        lines = file.readlines()

    professors: list[str] = []

    for i in range(len(lines)):
        line = lines[i]

        _list = line.split(",")
        professor_name, courses_list = _list[0], _list[1:]

        for course in all_courses:
            if course.title in courses_list:
                course.professor = professor_name

        professors.append(professor_name)
    
    return professors
