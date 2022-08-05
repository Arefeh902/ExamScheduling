
SLOT_PER_DAY = 3


class Course:
    title: str
    professor: str
    students_ids: list[int]  # student ids

    def __init__(self, title: str, professor: str, students_ids: list[int]):
        self.title = title
        self.professor = professor
        self.students_ids = students_ids

    def __str__(self):
        return self.title


class Student:
    pk: int
    courses: list[Course]

    def __init__(self, pk: int, courses: list[Course]):
        self.pk = pk
        self.courses = courses

    def __str__(self):
        return str(self.pk)


class TimeSlot:
    pk: int              # timeslot pks to find exam distances
    is_available: bool   # for eliminating restricted dates
    is_holiday: bool

    def __init__(self, pk: int, is_available: bool = True, is_holiday: bool = False):
        self.pk = pk
        self.is_available = is_available
        self.is_holiday = is_holiday

    def __str__(self):
        return f'Day:{self.pk // SLOT_PER_DAY} Slot:{self.pk % SLOT_PER_DAY}'


class Schedule:
    time_to_course: dict[TimeSlot: list[Course]]
    course_to_time: dict[Course: TimeSlot]
    fitness: int

    def __init__(self, time_slots: list[TimeSlot]):
        self.time_to_course = dict()
        self.course_to_time = dict()
        for slot in time_slots:
            self.time_to_course[slot] = list()
