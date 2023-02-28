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

        print('----------------------------')

        department_schedule: Schedule = Schedule(time_slots=time_slots)
        # department_schedule.time_to_course[time_slots[0]] = [courses[19], courses[2]]
        # department_schedule.time_to_course[time_slots[1]] = [courses[5]]
        # department_schedule.time_to_course[time_slots[2]] = [courses[16]]
        #
        # department_schedule.time_to_course[time_slots[3]] = [courses[21]]
        # department_schedule.time_to_course[time_slots[4]] = [courses[23]]
        # department_schedule.time_to_course[time_slots[5]] = []
        #
        # department_schedule.time_to_course[time_slots[6]] = [courses[12], courses[17]]
        # department_schedule.time_to_course[time_slots[7]] = [courses[22]]
        # department_schedule.time_to_course[time_slots[8]] = []
        #
        # department_schedule.time_to_course[time_slots[18]] = [courses[0], courses[27]]
        # department_schedule.time_to_course[time_slots[19]] = [courses[7], courses[14]]
        # department_schedule.time_to_course[time_slots[20]] = [courses[8]]
        #
        # department_schedule.time_to_course[time_slots[21]] = [courses[24]]
        # department_schedule.time_to_course[time_slots[22]] = [courses[26]]
        # department_schedule.time_to_course[time_slots[23]] = []
        #
        # department_schedule.time_to_course[time_slots[24]] = [courses[4]]
        # department_schedule.time_to_course[time_slots[25]] = [courses[25]]
        # department_schedule.time_to_course[time_slots[26]] = [courses[3]]
        #
        # department_schedule.time_to_course[time_slots[27]] = [courses[1]]
        # department_schedule.time_to_course[time_slots[28]] = [courses[10], courses[20]]
        # department_schedule.time_to_course[time_slots[29]] = [courses[13], courses[6]]


        # department_schedule.time_to_course[0] = ["مباني كامپيوتر و برنامه نويسي", "انتقال داده ها"]
        # department_schedule.time_to_course[1] = ["مدارهاي الكتريكي"]
        # department_schedule.time_to_course[2] = ["مدارهاي الكترونيكي"]

        # department_schedule.time_to_course[3] = ["اصول طراحي پايگاه داده ها"]
        # department_schedule.time_to_course[4] = ["تجارت الكترونيكي"]
        # department_schedule.time_to_course[5] = []
        #
        # department_schedule.time_to_course[6] = ["نظريه زبانهاوماشين", "شبكه هاي كامپيوتري"]
        # department_schedule.time_to_course[7] = ["طراحي و تحليل الگوريتمها"]
        # department_schedule.time_to_course[8] = []
        #
        # department_schedule.time_to_course[21] = ["برنامه نويسي پيشرفته", "برنامه نويسي شي گرا"]
        # department_schedule.time_to_course[22] = ["رياضي مهندسي", "ريزپردازنده"]
        # department_schedule.time_to_course[23] = ["معماري كامپيوتر"]
        #
        # department_schedule.time_to_course[24] = ["سيگنالهاوسيستمها"]
        # department_schedule.time_to_course[25] = ["نظريه و الگوريتم هاي گراف"]
        # department_schedule.time_to_course[26] = []
        #
        # department_schedule.time_to_course[27] = ["ساختمان داده هاوالگوريتمها 1"]
        # department_schedule.time_to_course[28] = ["هوش مصنوعي"]
        # department_schedule.time_to_course[29] = ["زبان ماشين و برنامه سازي سيستم"]
        #
        # department_schedule.time_to_course[30] = ["مباني تحقيق درعمليات"]
        # department_schedule.time_to_course[31] = ["اصول طراحي سيستم هاي عامل", "طراحي وپياده سازي زبانهاي برنامه سازي"]
        # department_schedule.time_to_course[32] = ["روشهاي محاسبات عددي", "مدارهاي منطقي"]
        #
        # department_schedule.fitness = genetic_algo.calculate_fitness(department_schedule)


        # last_schedule = department_schedule

    # last_schedule.get_csv_export()
    return last_schedule.to_json()

