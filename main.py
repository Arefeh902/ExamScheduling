from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO
from models import Course, Student, TimeSlot, Schedule
from read_data import read_courses_data, read_students_data, read_professors_data, read_time_slots_data
from ga import GeneticAlgorithm
from constraints.soft_constraints import calculate_penalty_of_student

app = Flask("Exam Scheduling")
CORS(app)
socketio = SocketIO(app)


@app.post("/")
def get_schedule():
    content = request.get_json()
    courses: list[Course] = read_courses_data(content["courses"])
    students: list[Student] = read_students_data(content["students"], courses)
    professors: list[str] = read_professors_data(content["professors"], courses)
    time_slots: list[TimeSlot] = read_time_slots_data(content["time_slots"])
    available_time_slots = TimeSlot.get_available_time_slots(time_slots)
    hyper_parameters_list: list[dict[str, int]] = content["hyper_parameters_list"]

    last_fitness = 0
    last_schedule = None

    for parameters in hyper_parameters_list:

        for header in parameters:
            print(f'{header}: {parameters[header]}, ', end='')
        print()

        socketio.emit("params", {"message": parameters}, broadcast=False)

        genetic_algo: GeneticAlgorithm = GeneticAlgorithm(population_size=parameters["population_size"],
                                                          max_generation=parameters["max_generation"],
                                                          mutation_probability=parameters["mutation_probability"],
                                                          courses=courses,
                                                          students=students,
                                                          professors=professors,
                                                          time_slots=available_time_slots,
                                                          time_slot_per_day=content['number_of_slots_per_day'],
                                                          calculate_penalty_of_student=calculate_penalty_of_student
                                                          )

        for _ in range(content["number_of_tries"]):
            schedule: Schedule = genetic_algo.generate_schedule()

            if schedule.fitness > last_fitness:
                last_fitness = schedule.fitness
                last_schedule = schedule

            socketio.emit("display fitness", {"message": f"try: {_ + 1}\tfitness: {schedule.fitness}"}, broadcast=False)
            print(f'try: {_ + 1}\n\tfitness: {schedule.fitness}')

        print('----------------------------')

    last_schedule.print()
    return last_schedule.to_json()


app.run()
