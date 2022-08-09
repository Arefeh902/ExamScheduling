from models import TimeSlot, Schedule, SLOT_PER_DAY
from utils import get_sorted_mean
from ga import GeneticAlgorithm
from soft_constraints import calculate_penalty_of_student
from read_data import read_student_and_course_data

NUM_OF_DAYS: int = 12
NUM_OF_RUNNING = 10


def test_different_params(path_to_input_file: str, num_of_days: int = NUM_OF_DAYS):
    professors: list[str] = []

    courses, students = read_student_and_course_data(path_to_input_file)

    time_slots: list[TimeSlot] = [TimeSlot(id) for id in range(num_of_days*SLOT_PER_DAY)]
    population_sizes: list[int] = [i for i in range(100, 601, 100)]
    max_generations: list[int] = [i for i in range(100, 301, 100)]
    mutation_probs: list[float] = [i/10 for i in range(4, 10)]

    path_to_output_file: str = ''.join(path_to_input_file.split('.')[:-1]) + '_output.txt'
    output_file = open(path_to_output_file, 'w')
    output_file.write(f'population_size max_generation mutation_prob')

    for population_size in population_sizes:
        for max_generation in max_generations:
            for mutation_prob in mutation_probs:

                output_file.write(f'\n{population_size} {max_generation} {mutation_prob}\n')

                print(population_size, max_generation, mutation_prob)
                
                for _ in range(NUM_OF_RUNNING):
                    genetic_algo: GeneticAlgorithm = GeneticAlgorithm(population_size=population_size,
                                                                      max_generation=max_generation,
                                                                      mutation_probability=mutation_prob,
                                                                      courses=courses,
                                                                      students=students,
                                                                      professors=professors,
                                                                      time_slots=time_slots,
                                                                      time_slot_per_day=SLOT_PER_DAY,
                                                                      calculate_penalty_of_student=
                                                                      calculate_penalty_of_student
                                                                      )
                    schedule: Schedule = genetic_algo.genetic_algorithm()

                    output_file.write(f'{schedule.fitness} ')

    output_file.close()

    get_sorted_mean(path_to_output_file)
