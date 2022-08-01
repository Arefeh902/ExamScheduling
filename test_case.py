from models import Course, TimeSlot, Schedule

test_time_slots: list[TimeSlot] = list()
for i in range(5):
    test_time_slots.append(TimeSlot(3*i))
    test_time_slots.append(TimeSlot(3*i + 1))
    test_time_slots.append(TimeSlot(3*i + 2))
