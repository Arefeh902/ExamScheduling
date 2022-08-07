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

NUM_OF_DAYS: int = 14
for i in range(NUM_OF_DAYS*SLOT_PER_DAY):
    time_slots.append(TimeSlot(i))

# create GeneticAlgorithm class and call genetic_algorithm
genetic_algo: GeneticAlgorithm = GeneticAlgorithm(population_size=500,
                                                  max_generation=10,
                                                  mutation_probability=0.3,
                                                  courses=courses,
                                                  students=students,
                                                  professors=[],
                                                  time_slots=time_slots,
                                                  time_slot_per_day=SLOT_PER_DAY,
                                                  calculate_penalty_of_student=calculate_penalty_of_student
                                                  )
schedule: Schedule = genetic_algo.genetic_algorithm()

# print results
print(schedule.fitness)
while schedule.fitness == 1:
    schedule = genetic_algo.genetic_algorithm()
    print(schedule.fitness)
schedule.print()

