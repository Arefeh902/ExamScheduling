from flask import Flask, request
from flask_cors import CORS
from models import Course, Student, TimeSlot, Schedule
from read_data import read_courses_data, read_students_data, read_professors_data, read_time_slots_data
from ga import GeneticAlgorithm
from constraints.soft_constraints import calculate_penalty_of_student
from utils import convert_csv_to_xlsx
import logging

# Create and configure logger
logging.basicConfig(filename="newfile.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


app = Flask("Exam Scheduling")
CORS(app)


@app.post("/")
def get_schedule():
    content = request.get_json()
    courses: list[Course] = read_courses_data(content["courses"])
    students: list[Student] = read_students_data(content["students"], courses)
    professors: list[str] = read_professors_data(content["professors"], courses)
    time_slots: list[TimeSlot] = read_time_slots_data(content["time_slots"])
    available_time_slots = TimeSlot.get_available_time_slots(time_slots)
    hyper_parameters_list: list[dict[str, int]] = content["hyper_parameters_list"]
    hyper_parameters_list += [
                              # {"population_size": 600, "max_generation": 600, "mutation_probability": 0.3},
                              # {"population_size": 700, "max_generation": 400, "mutation_probability": 0.3},
                              # {"population_size": 800, "max_generation": 500, "mutation_probability": 0.3},
                              # {"population_size": 1000, "max_generation": 450, "mutation_probability": 0.3},
                              # {"population_size": 600, "max_generation": 400, "mutation_probability": 0.4},
                              # {"population_size": 700, "max_generation": 400, "mutation_probability": 0.4},
                              # {"population_size": 800, "max_generation": 500, "mutation_probability": 0.4},
                              # {"population_size": 1000, "max_generation": 450, "mutation_probability": 0.4},
                              ]
    slot_per_day: int = content["number_of_slots_per_day"]
    Schedule.SLOT_PER_DAY = slot_per_day
    TimeSlot.SLOT_PER_DAY = slot_per_day

    last_schedule = None

    for parameters in hyper_parameters_list:

        for header in parameters:
            print(f'{header}: {parameters[header]}, ', end='')
            logger.info(f'{header}: {parameters[header]}')
        print()

        genetic_algo: GeneticAlgorithm = GeneticAlgorithm(population_size=parameters["population_size"],
                                                          max_generation=parameters["max_generation"],
                                                          mutation_probability=parameters["mutation_probability"],
                                                          courses=courses,
                                                          students=students,
                                                          professors=professors,
                                                          time_slots=time_slots,
                                                          available_time_slots=available_time_slots,
                                                          time_slot_per_day=slot_per_day,
                                                          calculate_penalty_of_student=calculate_penalty_of_student
                                                          )

        for _ in range(content["number_of_tries"]):
            schedule: Schedule = genetic_algo.generate_schedule()

            if last_schedule is None:
                last_schedule = schedule
            elif schedule.fitness > last_schedule.fitness:
                last_schedule = schedule

            logger.info(f'try: {_ + 1}\n\tfitness: {schedule.fitness}')
            print(f'try: {_ + 1}\n\tfitness: {schedule.fitness}')

        print('----------------------------')

    last_schedule.get_csv_export()
    return last_schedule.to_json()

