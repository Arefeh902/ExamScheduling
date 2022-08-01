from models import Course, TimeSlot, Schedule
from typing import Callable
import random


class GeneticAlgorithm:

    def __init__(self,
                 population_size: int,
                 max_generation: int,
                 crossover_probability: float,
                 mutation_probability: float,
                 courses: list[Course],
                 time_slots: list[TimeSlot],
                 time_slot_per_day: int,
                 fitness_func: Callable[[Schedule], int]
                 ):
        self.population_size = population_size
        self.max_generation = max_generation
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.courses = courses
        self.time_slots = time_slots
        self.time_slots_per_day = time_slot_per_day
        self.fitness_func = fitness_func
        self.num_of_time_slots = len(time_slots)
        self.current_population: list[Schedule] = list()

    def generate_random_solution(self) -> Schedule:
        schedule: Schedule = Schedule(self.time_slots)
        for course in self.courses:
            slot: TimeSlot = random.choice(self.time_slots)
            schedule[slot].appen(course)
        return schedule

    def generate_population(self) -> list[Schedule]:
        population: list[Schedule] = list()
        for _ in range(self.population_size):
            population.append(self.generate_random_solution())
        return population

    def select_parents(self) -> tuple[Schedule, Schedule]:
        pass

    def crossover(self, parent_a: Schedule, parent_b: Schedule) -> Schedule:
        pass

    def mutate(self, schedule: Schedule) -> Schedule:
        pass

    def get_next_generation(self):
        pass

    def genetic_algorithm(self) -> Schedule:
        pass
