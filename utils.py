import pandas as pd
from statistics import mean

from models import Schedule, Student

def convert_xlsx_to_csv(path_to_file: str) -> str:
    file = pd.read_excel(path_to_file)
    csv_file_name: str = ''.join(path_to_file.split('.')[:-1]) + '.csv'
    file.to_csv(csv_file_name)
    return csv_file_name


def get_mean(path_to_input_file: str):
    input_file = open(path_to_input_file)
    path_to_output_file: str = ''.join(path_to_input_file.split('.')[:-1]) + '_output.txt'
    output_file = open(path_to_output_file, 'w')

    lines = input_file.readlines()
    for i in range(1, len(lines), 2):
        output_file.write(f'{lines[i]} ')

        l = lines[i + 1].split(' ')[:-1]
        l = [int(x) for x in l]

        output_file.write(f'{sum(l) / len(l)}\n')


def get_sorted_mean(path_to_input_file: str, include_no_result: bool = True):
    
    lines = []
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

def get_student_time_slots(schedule: Schedule, student: Student) -> list[int]:
    times: list[int] = []

    for course in student.courses:
        times.append(schedule.get_course_time(course).pk)

    times.sort()

    return times