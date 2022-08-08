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

mutation_probs: list[float] = []
for i in range(10):
    mutation_probs.append(i/10)

population_sizes: list[int] = []
for i in range(100, 1000, 100):
    population_sizes.append(i)

max_generations: list[int] = []
for i in range(50, 500, 50):
    max_generations.append(i)

NUM_OF_RUNNING = 10
result = open('results.txt', 'w')

# create GeneticAlgorithm class and call genetic_algorithm
result.write(f'population_size max_generation mutation_prob')
for population_size in population_sizes:
    for max_generation in max_generations:
        for mutation_prob in mutation_probs:
            result.write(f'\n{population_size} {max_generation} {mutation_prob}\n')
            for _ in range(NUM_OF_RUNNING):
                genetic_algo: GeneticAlgorithm = GeneticAlgorithm(population_size=population_size,
                                                                  max_generation=max_generation,
                                                                  mutation_probability=mutation_prob,
                                                                  courses=courses,
                                                                  students=students,
                                                                  professors=[],
                                                                  time_slots=time_slots,
                                                                  time_slot_per_day=SLOT_PER_DAY,
                                                                  calculate_penalty_of_student=
                                                                  calculate_penalty_of_student
                                                                  )
                schedule: Schedule = genetic_algo.genetic_algorithm()
                result.write(f'{schedule.fitness} ')
