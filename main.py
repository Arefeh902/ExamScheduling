from models import TimeSlot, Schedule
from ga import GeneticAlgorithm
from constraints.soft_constraints import calculate_penalty_of_student
from read_data import read_student_and_course_data
from utils import convert_csv_to_xlsx
from config import get_config_dict

from vars import hyper_parameters_list

Config = get_config_dict()

time_slots: list[TimeSlot] = [TimeSlot(i) for i in range(Config["number_of_days"] * Config['number_of_slots_per_day'])]
professors: list[str] = []


courses, students = read_student_and_course_data('data/naft_data.csv')


last_fitness = 0
last_schedule = None

for parameters in hyper_parameters_list:

    print(parameters)

    genetic_algo: GeneticAlgorithm = GeneticAlgorithm(population_size=parameters["population_size"],
                                                      max_generation=parameters["max_generation"],
                                                      mutation_probability=parameters["mutation_probability"],
                                                      courses=courses,
                                                      students=students,
                                                      professors=[],
                                                      time_slots=time_slots,
                                                      time_slot_per_day=Config['number_of_slots_per_day'],
                                                      calculate_penalty_of_student=calculate_penalty_of_student
                                                      )

    for _ in range(Config["number_of_tries"]):
        schedule: Schedule = genetic_algo.generate_schedule()

        if schedule.fitness > last_fitness:
            last_fitness = schedule.fitness
            last_schedule = schedule

        print(schedule.fitness)

    print('---------------')

schedule.print()
convert_csv_to_xlsx(schedule.get_csv_export())
