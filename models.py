import csv
import json


class Course:
    title: str
    professor: str
    students_ids: list[int]
    is_first_or_second_year_course: bool
    pk: int

    def __init__(self, pk: int, title: str, professor: str, students_ids: list[int], is_first: bool = False):
        self.pk = pk
        self.title = title
        self.professor = professor
        self.students_ids = students_ids
        self.is_first_or_second_year_course = is_first

    def __str__(self):
        return str(self.pk) + " " + str(self.title)

    def __repr__(self):
        return self.title

    @staticmethod
    def get_course_by_title(courses, title: str):
        for course in courses:
            if course.title == title:
                return course
        return None

    @staticmethod
    def get_course_by_id(courses, pk: int):
        for course in courses:
            if course.pk == pk:
                return course
        return None

    @staticmethod
    def join_course_titles(courses) -> str:
        res: str = ''
        for course in courses:
            res += f'{course.title} '
        return res

    def serialize(self):
        return {"title": self.title, "professor": self.professor, "student_ids": self.students_ids}


class Student:
    pk: int
    courses: list[int]

    def __init__(self, pk: int, courses: list[int]):
        self.pk = pk
        self.courses = courses

    def __str__(self):
        return str(self.pk) + " " + str(self.courses)


class TimeSlot:
    pk: int
    is_available: bool
    is_holiday: bool
    has_general_exam: bool
    SLOT_PER_DAY: int = 3

    def get_day(self):
        return (self.pk - 1) // self.SLOT_PER_DAY

    def get_slot(self):
        return (self.pk - 1) % self.SLOT_PER_DAY

    def __init__(self, pk: int, is_available: bool = True, is_holiday: bool = False, has_general_exam: bool = False):
        self.pk = pk
        self.is_available = is_available
        self.is_holiday = is_holiday
        self.has_general_exam = has_general_exam

    def __str__(self):
        return f'Day:{self.get_day()} Slot:{self.get_slot()}, Able:{self.is_available}'

    def __repr__(self):
        return f'Day:{self.get_day()} Slot:{self.get_slot()}'

    def __cmp__(self, other):
        if self.pk <= other.pk:
            return True
        return False

    def __lt__(self, other):
        return self.pk < other.pk

    def __gt__(self, other):
        return self.pk > other.pk

    @staticmethod
    def get_available_time_slots(time_slots):
        return [time for time in time_slots if time.is_available]


class Schedule:
    time_to_course: dict[TimeSlot: Course]
    fitness: int

    two_exams_in_one_day: int
    two_consecutive_exams: int
    three_consecutive_exams: int
    exams_on_holiday: int
    single_day_rest: int

    students_with_two_exams_in_one_day: int
    students_with_two_consecutive_exams: int
    students_with_three_consecutive_exams: int
    students_with_exams_on_holiday: int
    students_with_single_day_rest: int

    SLOT_PER_DAY: int = 3

    def __init__(self, time_slots: list[TimeSlot]):
        self.time_to_course = dict()
        self.two_exams_in_one_day = 0
        self.two_consecutive_exams = 0
        self.three_consecutive_exams = 0
        self.exams_on_holiday = 0
        self.single_day_rest = 0

        self.students_with_two_exams_in_one_day = 0
        self.students_with_two_consecutive_exams = 0
        self.students_with_three_consecutive_exams = 0
        self.students_with_exams_on_holiday = 0
        self.students_with_single_day_rest = 0
        for slot in time_slots:
            self.time_to_course[slot] = list()

    def get_course_time(self, course: Course) -> TimeSlot:
        for time in self.time_to_course:
            if course in self.time_to_course[time]:
                return time

    def get_course_time_by_id(self, course_id: int) -> TimeSlot:
        for time in self.time_to_course:
            for course in self.time_to_course[time]:
                if course_id == course.pk:
                    return time

    def get_courses_in_time_slot(self, time: TimeSlot) -> list[Course]:
        if not time:
            return []
        return self.time_to_course[time]

    def get_courses(self) -> list[Course]:
        courses: list[Course] = []
        for time in self.time_to_course:
            courses.extend(self.time_to_course[time])
        return courses

    def print(self):
        for time in self.time_to_course:
            print(time, end=' ')
            for c in self.time_to_course[time]:
                print(c, end=' ')
            print()
            if time.get_slot() == self.SLOT_PER_DAY - 1:
               print()

    def get_csv_export(self, file_name: str = 'schedule.csv') -> str:
        export_file_path = f'schedules/{file_name}'

        with open(export_file_path, 'w') as export_file:
            writer = csv.writer(export_file)

            header: list[str] = ['ردیف']
            for i in range(self.SLOT_PER_DAY):
                header.append(str(i + 1))
            writer.writerow(header)

            day_id: int = 0
            data: list[str] = [str(day_id)] + [''] * self.SLOT_PER_DAY
            for time in sorted(list(self.time_to_course)):
                if time.pk // self.SLOT_PER_DAY != day_id:
                    writer.writerow(data)
                    day_id += 1
                    while day_id != time.pk // self.SLOT_PER_DAY:
                        writer.writerow([day_id])
                        day_id += 1
                    data = [str(day_id)] + [''] * self.SLOT_PER_DAY

                data[time.pk % self.SLOT_PER_DAY + 1] += Course.join_course_titles(self.time_to_course[time])

            writer.writerow(data)

        return export_file_path

    def to_json(self):
        schedule_data = []
        for time in self.time_to_course:
            schedule_data.append({"time_slot": time.pk, "courses": [course.serialize() for course in self.time_to_course[time]]})

        data = {"schedule": schedule_data, "fitness": self.fitness,

                "two_exams_in_one_day": self.two_exams_in_one_day,
                "students_with_two_exams_in_one_day": self.students_with_two_exams_in_one_day,

                "two_consecutive_exams": self.two_consecutive_exams,
                "student_with_two_consecutive_exams": self.students_with_two_consecutive_exams,

                "three_consecutive_exams": self.three_consecutive_exams,
                "students_with_three_consecutive_exams": self.students_with_three_consecutive_exams,

                }
        return json.dumps(data, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)
