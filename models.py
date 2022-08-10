import csv

SLOT_PER_DAY = 3


class Course:
    title: str
    professor: str
    students_ids: list[int]

    def __init__(self, title: str, professor: str, students_ids: list[int]):
        self.title = title
        self.professor = professor
        self.students_ids = students_ids

    def __str__(self):
        return self.title

    @staticmethod
    def join_course_titles(courses) -> str:
        res: str = ''
        for course in courses:
            res += f'{course.title} '
        return res


class Student:
    pk: int
    courses: list[Course]

    def __init__(self, pk: int, courses: list[Course]):
        self.pk = pk
        self.courses = courses

    def __str__(self):
        return str(self.pk)


class TimeSlot:
    pk: int
    is_available: bool
    is_holiday: bool

    def __init__(self, pk: int, is_available: bool = True, is_holiday: bool = False):
        self.pk = pk
        self.is_available = is_available
        self.is_holiday = is_holiday

    def __str__(self):
        return f'Day:{self.pk // SLOT_PER_DAY} Slot:{self.pk % SLOT_PER_DAY}'

    def get_day(self):
        return self.pk // SLOT_PER_DAY

    def __cmp__(self, other):
        if self.pk <= other.pk:
            return True
        return False

    def __lt__(self, other):
        return self.pk < other.pk

    def __gt__(self, other):
        return self.pk > other.pk


class Schedule:
    time_to_course: dict[TimeSlot: list[Course]]
    fitness: int

    def __init__(self, time_slots: list[TimeSlot]):
        self.time_to_course = dict()
        for slot in time_slots:
            self.time_to_course[slot] = list()

    def get_course_time(self, course: Course) -> TimeSlot:
        for time in self.time_to_course:
            if course in self.time_to_course[time]:
                return time

    def get_courses_in_time_slot(self, time: TimeSlot) -> list[Course]:
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
            if time.pk % SLOT_PER_DAY == SLOT_PER_DAY - 1:
                print()

    def get_csv_export(self, file_name: str = 'schedule.csv') -> str:
        export_file_path = f'schedules/{file_name}'

        with open(export_file_path, 'w') as export_file:
            writer = csv.writer(export_file)

            header: list[str] = ['ردیف']
            for i in range(SLOT_PER_DAY):
                header.append(str(i + 1))
            writer.writerow(header)

            day_id: int = 0
            data: list[str] = [str(day_id)] + [''] * SLOT_PER_DAY
            for time in sorted(list(self.time_to_course)):
                if time.pk // SLOT_PER_DAY != day_id:
                    writer.writerow(data)
                    day_id += 1
                    while day_id != time.pk // SLOT_PER_DAY:
                        writer.writerow([day_id])
                        day_id += 1
                    data = [str(day_id)] + [''] * SLOT_PER_DAY

                data[time.pk % SLOT_PER_DAY + 1] += Course.join_course_titles(self.time_to_course[time])

            writer.writerow(data)

        return export_file_path
