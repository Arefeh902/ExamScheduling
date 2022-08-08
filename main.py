from models import Course, Student, TimeSlot, Schedule, SLOT_PER_DAY
from ga import GeneticAlgorithm
from constraints import calculate_penalty_of_student
from read_data import read_student_and_course_data

# load data
time_slots: list[TimeSlot] = []
# courses: list[Course] = []
# students: list[Student] = []
professors: list[str] = []

courses, students = read_student_and_course_data('data/naft_data.csv')

NUM_OF_DAYS: int = 12
for i in range(NUM_OF_DAYS*SLOT_PER_DAY):
    time_slots.append(TimeSlot(i))

hyper_parameters_list = [
    {
        "population_size": 600,
        "max_generation": 300,
        "mutation_probability": 0.9
    },
    {
        "population_size": 600,
        "max_generation": 300,
        "mutation_probability": 0.6
    },
    {
        "population_size": 500,
        "max_generation": 200,
        "mutation_probability": 0.9
    },
    {
        "population_size": 500,
        "max_generation": 200,
        "mutation_probability": 0.6
    },
]

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
                                                    time_slot_per_day=SLOT_PER_DAY,
                                                    calculate_penalty_of_student=calculate_penalty_of_student
    )

    for _ in range(5):
        schedule: Schedule = genetic_algo.genetic_algorithm()

        if schedule.fitness > last_fitness:
            last_fitness = schedule.fitness
            last_schedule = schedule

        print(schedule.fitness)

    print('---------------')
schedule.print()