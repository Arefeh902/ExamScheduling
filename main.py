from flask import Flask, request
from flask_socketio import SocketIO
from models import Course, Student, TimeSlot
from read_data import read_courses_data, read_students_data, read_professors_data

app = Flask("Exam Scheduling")
socketio = SocketIO(app)


@app.post("/get-schedule/")
def get_schedule():
    content = request.get_json()
    courses: list[Course] = read_courses_data(content["courses"])
    students: list[Student] = read_students_data(content["students"], courses)
    professors: list[str] = read_professors_data(content["professor"], courses)
    # time_slots: list[TimeSlot] = read_time_slot_data(content["time_slots"])

    return "<p>Hello, World!</p>"
