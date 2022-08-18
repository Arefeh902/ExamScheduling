import pandas as pd
from statistics import mean
from models import Schedule, Student, TimeSlot, Course


def convert_xlsx_to_csv(path_to_file: str) -> str:
    file = pd.read_excel(path_to_file)
    csv_file_name: str = ''.join(path_to_file.split('.')[:-1]) + '.csv'
    file.to_csv(csv_file_name)
    return csv_file_name


def convert_csv_to_xlsx(path_to_file: str) -> str:
    file = pd.read_csv(path_to_file)
    xlsx_file_name: str = ''.join(path_to_file.split('.')[:-1]) + '.xlsx'
    file.to_excel(xlsx_file_name, index=None, header=True)
    return xlsx_file_name


def get_sorted_mean(path_to_input_file: str, include_no_result: bool = True):

    with open(path_to_input_file) as input_file:
        lines = input_file.readlines()

    output_list = []
    for i in range(1, len(lines), 2):
        output_text = lines[i].split(' ')
        output_text[-1] = output_text[-1][:-1]

        fitness_values = lines[i + 1].split(' ')[:-1]
        if include_no_result:
            fitness_values = [int(x) for x in fitness_values]
        else:
            fitness_values = [int(x) for x in fitness_values if int(x) != 1]

        output_list.append([mean(fitness_values), output_text])

    output_list.sort(reverse=True)

    path_to_output_file: str = ''.join(path_to_input_file.split('.')[:-1]) + '_sorted_output.txt'
    with open(path_to_output_file, 'w') as output_file:
        for fitness in output_list:
            output_file.write(f'{fitness[0]} {fitness[1]}\n')


def get_student_time_slots(schedule: Schedule, student: Student) -> list[TimeSlot]:
    times: list[TimeSlot] = []

    for course_id in student.courses:
        times.append(schedule.get_course_time(Course.get_course_by_id(schedule.get_courses(), course_id)))

    times.sort()

    return times
