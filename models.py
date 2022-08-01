
class Course:
    course: str
    professor: str
    students: list[int]  # student ids


class TimeSlot:
    pk: int              # timeslot pks to find exam distances
    is_available: bool   # for eliminating restricted dates

    def __init__(self, pk: int, is_available: bool = True):
        self.pk = pk
        self.is_available = is_available

    def __str__(self):
        return f'Day:{self.pk // 3} Slot:{self.pk % 3}'


class Schedule:
    mapping: dict[TimeSlot: list[Course]]
    fitness: int

    def __init__(self, time_slots: list[TimeSlot]):
        self.mapping = dict()
        for slot in time_slots:
            self.mapping[slot] = list()
