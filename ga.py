from models import Course, Student, TimeSlot, Schedule
from typing import Callable
import random
from hard_constraints import check_hard_constraints


class GeneticAlgorithm:

    MAX_FITNESS: int = 100000000
    MAX_RANDOM_TRY: int = 1000

    def __init__(self,
                 population_size: int,
                 max_generation: int,
                 mutation_probability: float,
                 courses: list[Course],
                 students: list[Student],
                 professors: list[str],
                 time_slots: list[TimeSlot],
                 time_slot_per_day: int,
                 calculate_penalty_of_student: Callable[[Schedule, Student], int]
                 ):
        self.population_size = population_size
        self.max_generation = max_generation
        self.mutation_probability = mutation_probability
        self.courses = courses
        self.students = students
        self.professors = professors
        self.time_slots = time_slots
        self.time_slots_per_day = time_slot_per_day
        self.calculate_penalty_of_student = calculate_penalty_of_student
        self.num_of_time_slots = len(time_slots)
        self.current_population: list[Schedule] = list()
        self.pool: list[int] = [0] * self.population_size

    @staticmethod
    def courses_have_intersection(course1: Course, course2: Course) -> bool:
        if len(set(course1.students_ids) & set(course2.students_ids)) > 0:
            return True
        return False

    def calculate_fitness(self, schedule: Schedule) -> int:
        fit: int = GeneticAlgorithm.MAX_FITNESS

        if not check_hard_constraints(schedule, self):
            return 1

        for student in self.students:
            fit -= self.calculate_penalty_of_student(schedule, student)
        
        return fit

    def get_slot_by_pk(self, pk: int) -> TimeSlot:
        for slot in self.time_slots:
            if slot.pk == pk:
                return slot
        return None

    def generate_random_solution(self) -> Schedule:
        schedule: Schedule = Schedule(self.time_slots)

        for course in self.courses:
            slot: TimeSlot = random.choice(self.time_slots)

            for _ in range(GeneticAlgorithm.MAX_RANDOM_TRY):
                day: int = slot.pk // self.time_slots_per_day
                same_day_slots: list[TimeSlot] = []

                for i in range(self.time_slots_per_day):
                    same_day_slots.append(self.get_slot_by_pk(day + i))

                have_intersection: bool = False
                for day_ in same_day_slots:
                    for course_ in schedule.get_courses_in_time_slot(day_):
                            
                        if len(set(course.students_ids) & set(course_.students_ids)) > 0:
                            have_intersection = True
                            break

                    if have_intersection:
                        break
                
                if not have_intersection:
                    break

                slot = random.choice(self.time_slots)

            schedule.get_courses_in_time_slot(slot).append(course)

        return schedule

    def generate_population(self) -> list[Schedule]:
        return [self.generate_random_solution() for _ in self.population_size]

    def create_pool(self):
        self.pool[1] = self.current_population[0].fitness

        for i in range(1, len(self.current_population)):
            self.pool[i] = self.pool[i-1] + self.current_population[i].fitness

    def get_parents(self) -> tuple[Schedule, Schedule]:
        rand_a: int = random.randint(1, self.pool[self.population_size-1])
        rand_b: int = random.randint(1, self.pool[self.population_size-1])

        for i in range(self.population_size):
            if rand_a <= self.pool[i]:
                rand_a = i

        for i in range(self.population_size):
            if rand_b <= self.pool[i]:
                rand_b = i
                
        parent_a: Schedule = self.current_population[rand_a]
        parent_b: Schedule = self.current_population[rand_b]

        return parent_a, parent_b

    def crossover(self) -> Schedule:
        parent_a, parent_b = self.get_parents()
        schedule: Schedule = Schedule(self.time_slots)

        for course in self.courses:

            if random.uniform(0, 1) <= 1/2:
                slot: TimeSlot = parent_a.get_course_time(course)
            else:
                slot: TimeSlot = parent_b.get_course_time(course)
            
            schedule.get_courses_in_time_slot(slot).append(course)

        return schedule

    def mutate(self, schedule: Schedule) -> Schedule:
        for course in self.courses:
            if random.uniform(0, 1) < self.mutation_probability:
                schedule.time_to_course[schedule.get_course_time(course)].remove(course)
                slot: TimeSlot = random.choice(self.time_slots)
                schedule.get_courses_in_time_slot(slot).append(course)

        return schedule

    def get_next_generation(self) -> list[Schedule]:
        population: list[Schedule] = []
        schedule: Schedule

        for _ in range(self.population_size):
            schedule = self.crossover()
            schedule = self.mutate(schedule)
            population.append(schedule)

        return population

    def generate_schedule(self) -> Schedule:
        self.current_population = self.generate_population()
        best_schedule: Schedule = self.current_population[0]

        for _ in range(self.max_generation):

            for schedule in self.current_population:
                schedule.fitness = self.calculate_fitness(schedule)

                if schedule.fitness > best_schedule.fitness:
                    best_schedule = schedule

            self.create_pool()

            self.current_population = self.get_next_generation()

        return best_schedule
