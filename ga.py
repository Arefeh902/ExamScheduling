from models import Course, Student, TimeSlot, Schedule
from typing import Callable
import random


MAX_FITNESS: int = 1000000000


class GeneticAlgorithm:

    def __init__(self,
                 population_size: int,
                 max_generation: int,
                 # crossover_probability: float,
                 mutation_probability: float,
                 courses: list[Course],
                 students: list[Student],
                 time_slots: list[TimeSlot],
                 time_slot_per_day: int,
                 penalty_per_student: Callable[[Schedule, Student], int]
                 ):
        self.population_size = population_size
        self.max_generation = max_generation
        # self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.courses = courses
        self.students = students
        self.time_slots = time_slots
        self.time_slots_per_day = time_slot_per_day
        self.penalty_per_student = penalty_per_student
        self.num_of_time_slots = len(time_slots)
        self.current_population: list[Schedule] = list()
        self.pool: list[Schedule] = []

    def fitness(self, schedule: Schedule) -> int:
        fit: int = MAX_FITNESS
        for student in self.students:
            fit -= self.penalty_per_student(schedule, student)
        return fit

    def generate_random_solution(self) -> Schedule:
        schedule: Schedule = Schedule(self.time_slots)
        for course in self.courses:
            slot: TimeSlot = random.choice(self.time_slots)
            schedule.time_to_course[slot].appen(course)
            schedule.course_to_time[course] = slot
        return schedule

    def generate_population(self) -> list[Schedule]:
        population: list[Schedule] = list()
        for _ in range(self.population_size):
            population.append(self.generate_random_solution())
        return population

    def create_pool(self):
        for schedule in self.current_population:
            for _ in range(schedule.fitness):
                self.pool.append(schedule)

    def select_parents(self) -> tuple[Schedule, Schedule]:
        parent_a: Schedule = random.choice(self.pool)
        parent_b: Schedule = random.choice(self.pool)
        while parent_b == parent_a:
            parent_b = random.choice(self.pool)
        return parent_a, parent_b

    def crossover(self) -> Schedule:
        parent_a, parent_b = self.select_parents()
        schedule: Schedule = Schedule(self.time_slots)
        for course in self.courses:
            if random.uniform(0, 1) <= 1/2:
                slot: TimeSlot = parent_a.course_to_time[course]
                schedule.time_to_course[slot].append(course)
                schedule.course_to_time[course] = slot
            else:
                slot: TimeSlot = parent_b.course_to_time[course]
                schedule.time_to_course[slot].append(course)
                schedule.course_to_time[course] = slot
        return schedule

    def mutate(self, schedule: Schedule) -> Schedule:
        for course in self.courses:
            if random.uniform(0, 1) < self.mutation_probability:
                schedule.time_to_course[schedule.course_to_time[course]].remove(course)
                slot: TimeSlot = random.choice(self.time_slots)
                schedule.time_to_course[slot].append(course)
                schedule.course_to_time[course] = slot
        return schedule

    def get_next_generation(self) -> list[Schedule]:
        population: list[Schedule] = []
        schedule: Schedule
        for _ in range(self.population_size):
            schedule = self.crossover()
            schedule = self.mutate(schedule)
            population.append(schedule)
        return population

    def genetic_algorithm(self) -> Schedule:
        self.current_population = self.generate_population()
        best_schedule: Schedule = self.current_population[0]

        for _ in range(self.max_generation):

            # calc fitness
            for schedule in self.current_population:
                schedule.fitness = self.fitness(schedule)
                if schedule.fitness > best_schedule.fitness:
                    best_schedule = schedule

            # create pool
            self.create_pool()

            # get next generation
            self.current_population = self.get_next_generation()

        return best_schedule
