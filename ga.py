from models import Course, TimeSlot, Schedule


class GeneticAlgorithm:

    def __init__(self,
                 population_size: int,
                 max_generation: int,
                 crossover_probability: float,
                 mutation_probability: float,
                 courses: list[Course],
                 time_slots: list[TimeSlot]
                 ):
        self.population_size = population_size
        self.max_generation = max_generation
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.courses = courses
        self.time_slots = time_slots

    def generate_population(self) -> list[Schedule]:
        pass

    def calc_fitness(self, schedule: Schedule) -> int:
        pass

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

    # def select_parents(population:)
