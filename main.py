from flask import Flask, request
from flask_cors import CORS
from models import Course, Student, TimeSlot, Schedule
from read_data import read_courses_data, read_students_data, read_professors_data, read_time_slots_data
from ga import GeneticAlgorithm
from constraints.soft_constraints import calculate_penalty_of_student
from utils import convert_csv_to_xlsx
import logging

# Create and configure logger
# logging.basicConfig(filename="newfile.log",
#                     format='%(asctime)s %(message)s',
#                     filemode='w')
# logger = logging.getLogger()
# logger.setLevel(logging.DEBUG)


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
        {"population_size": 100, "max_generation": 400, "mutation_probability": 0.01},
        {"population_size": 150, "max_generation": 400, "mutation_probability": 0.01},
        {"population_size": 200, "max_generation": 400, "mutation_probability": 0.01},
        {"population_size": 100, "max_generation": 400, "mutation_probability": 0.02},
        {"population_size": 150, "max_generation": 400, "mutation_probability": 0.02},
        {"population_size": 200, "max_generation": 400, "mutation_probability": 0.02},
        {"population_size": 100, "max_generation": 400, "mutation_probability": 0.03},
        {"population_size": 150, "max_generation": 400, "mutation_probability": 0.03},
        {"population_size": 200, "max_generation": 400, "mutation_probability": 0.03},
        {"population_size": 100, "max_generation": 400, "mutation_probability": 0.04},
        {"population_size": 150, "max_generation": 400, "mutation_probability": 0.04},
        {"population_size": 200, "max_generation": 400, "mutation_probability": 0.04},
        {"population_size": 100, "max_generation": 400, "mutation_probability": 0.05},
        {"population_size": 150, "max_generation": 400, "mutation_probability": 0.05},
        {"population_size": 200, "max_generation": 400, "mutation_probability": 0.05},
    ]
    slot_per_day: int = content["number_of_slots_per_day"]
    Schedule.SLOT_PER_DAY = slot_per_day
    TimeSlot.SLOT_PER_DAY = slot_per_day

    for course in courses:
        print(course)

    last_schedule = None

    for parameters in hyper_parameters_list:

        for header in parameters:
            print(f'{header}: {parameters[header]}, ', end='')
            # logger.info(f'{header}: {parameters[header]}')
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

            # logger.info(f'try: {_ + 1}\n\tfitness: {schedule.fitness}')
            print(f'try: {_ + 1}\n\tfitness: {schedule.fitness}')

        # print('----------------------------')

        # department_schedule: Schedule = Schedule(time_slots=time_slots)
        # department_schedule.time_to_course[time_slots[0]] = [courses[15], courses[2]]
        # department_schedule.time_to_course[time_slots[1]] = [courses[5]]
        # department_schedule.time_to_course[time_slots[2]] = [courses[13]]
        #
        # department_schedule.time_to_course[time_slots[3]] = [courses[17]]
        # department_schedule.time_to_course[time_slots[4]] = [courses[19]]
        # department_schedule.time_to_course[time_slots[5]] = []
        #
        # department_schedule.time_to_course[time_slots[6]] = [courses[10], courses[14]]
        # department_schedule.time_to_course[time_slots[7]] = [courses[18]]
        # department_schedule.time_to_course[time_slots[8]] = []
        #
        # department_schedule.time_to_course[time_slots[18]] = [courses[23], courses[0]]
        # department_schedule.time_to_course[time_slots[19]] = [courses[12], courses[7]]
        # department_schedule.time_to_course[time_slots[20]] = [courses[8]]
        #
        # department_schedule.time_to_course[time_slots[21]] = [courses[20]]
        # department_schedule.time_to_course[time_slots[22]] = [courses[22]]
        # department_schedule.time_to_course[time_slots[23]] = []
        #
        # department_schedule.time_to_course[time_slots[24]] = [courses[4]]
        # department_schedule.time_to_course[time_slots[25]] = [courses[21]]
        # department_schedule.time_to_course[time_slots[26]] = [courses[3]]
        #
        # department_schedule.time_to_course[time_slots[27]] = [courses[1]]
        # department_schedule.time_to_course[time_slots[28]] = [courses[9], courses[16]]
        # department_schedule.time_to_course[time_slots[29]] = [courses[6], courses[11]]

        # department_schedule.fitness = genetic_algo.calculate_fitness(department_schedule)
        # last_schedule = department_schedule

    last_schedule.get_csv_export()
    return last_schedule.to_json()
