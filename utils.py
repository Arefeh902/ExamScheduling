import pandas as pd


# helper functions - could be moved to utils file
def convert_xlsx_to_csv(path_to_file: str) -> str:
    file = pd.read_excel(path_to_file)
    csv_file_name: str = ''.join(path_to_file.split('.')[:-1]) + '.csv'
    file.to_csv(csv_file_name)
    return csv_file_name


def get_mean(path_to_input_file: str):
    input_file = open(path_to_input_file)
    path_to_output_file: str = ''.join(path_to_input_file.split('.')[:-1]) + 'output.txt'
    output_file = open(path_to_output_file, 'w')

    lines = input_file.readlines()
    for i in range(1, len(lines), 2):
        output_file.write(f'{lines[i]} ')

        l = lines[i + 1].split(' ')[:-1]
        l = [int(x) for x in l]

        output_file.write(f'{sum(l) / len(l)}\n')


def get_sorted_mean(path_to_input_file: str):
    input_file = open(path_to_input_file)
    path_to_output_file: str = ''.join(path_to_input_file.split('.')[:-1]) + 'sorted_output.txt'
    output_file = open(path_to_output_file, 'w')

    output_list = []

    lines = input_file.readlines()
    for i in range(1, len(lines), 2):
        l = lines[i + 1].split(' ')[:-1]
        l = [int(x) for x in l]

        output_list.append([sum(l) / len(l), lines[i].split(' ')])

    output_list.sort(reverse=True)

    for x in output_list:
        output_file.write(f'{x[0]} {x[1]}\n')


def get_sorted_mean_without_1s(path_to_input_file: str):
    input_file = open(path_to_input_file)
    path_to_output_file: str = ''.join(path_to_input_file.split('.')[:-1]) + 'sorted_without_1s_output.txt'
    output_file = open(path_to_output_file, 'w')

    output_list = []

    lines = input_file.readlines()
    for i in range(1, len(lines), 2):
        l = lines[i + 1].split(' ')[:-1]
        l = [int(x) for x in l if int(x) != 1]

        output_list.append([sum(l) / len(l), lines[i].split(' ')])

    output_list.sort(reverse=True)

    for x in output_list:
        output_file.write(f'{x[0]} {x[1]}\n')
