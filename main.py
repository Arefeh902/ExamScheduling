from models import Course, Student, TimeSlot, Schedule, SLOT_PER_DAY
from ga import GeneticAlgorithm
from constraints import penalty_per_student

# load data
courses: list[Course] = []
time_slots: list[TimeSlot] = []
students: list[Student] = []
professors: list[str] = []

with open('Naft_Data.txt', 'r') as file:
    lines = file.readlines()
    # read course names
    course_names: str = lines[0]
    course_names: list[str] = course_names.split('\t')
    for course in course_names:
        courses.append(Course(course, '', []))
    lines = lines[1:]
    for i in range(len(lines)):
        line: list[str] = lines[i].split('\t')
        student: Student = Student(int(line[0]), [])
        for j in range(1, len(line)):
            if line[j] == '1':
                # add student to course
                courses[j-1].students_ids.append(student.pk)
                # course to student
                student.courses.append(courses[j-1])
        students.append(student)

NUM_OF_DAYS: int = 15
for i in range(NUM_OF_DAYS*SLOT_PER_DAY):
    time_slots.append(TimeSlot(i))


# create GeneticAlgorithm class and call genetic_algorithm
genetic_algo: GeneticAlgorithm = GeneticAlgorithm(population_size=1000,
                                                  max_generation=500,
                                                  mutation_probability=0.001,
                                                  courses=courses,
                                                  students=students,
                                                  professors=[],
                                                  time_slots=time_slots,
                                                  time_slot_per_day=SLOT_PER_DAY,
                                                  penalty_per_student=penalty_per_student
                                                  )
schedule: Schedule = genetic_algo.genetic_algorithm()

# print results
print(schedule.fitness)
schedule.print()