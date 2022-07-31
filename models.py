
class Course:
    course: str
    professor: str
    students: list[int]  # student ids


class TimeSlot:
    id: int              # timeslot ids to find exam distances
    is_available: bool   # for eliminating restricted dates


class Schedule:
    mapping: dict[TimeSlot: list[Course]]
    fitness: int
