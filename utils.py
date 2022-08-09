import pandas as pd


# helper functions - could be moved to utils file
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


def get_sorted_mean(path_to_input_file: str, include_one: bool = True):
    input_file = open(path_to_input_file)
    path_to_output_file: str = ''.join(path_to_input_file.split('.')[:-1]) + '_sorted_output.txt'
    output_file = open(path_to_output_file, 'w')

    output_list = []

    lines = input_file.readlines()
    for i in range(1, len(lines), 2):
        output_text = lines[i].split(' ')
        output_text[-1] = output_text[-1][:-1]

        l = lines[i + 1].split(' ')[:-1]
        if include_one:
            l = [int(x) for x in l]
        else:
            l = [int(x) for x in l if int(x) != 1]

        output_list.append([sum(l) / len(l), output_text])

    output_list.sort(reverse=True)

    for x in output_list:
        output_file.write(f'{x[0]} {x[1]}\n')

def get_student_time_slots(schedule: Schedule, student: Student) -> list[int]:
    times: list[int] = []
    for course in student.courses:
        times.append(schedule.get_course_time(course).pk)

    times.sort()

    return times