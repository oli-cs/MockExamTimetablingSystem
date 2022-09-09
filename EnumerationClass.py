from enum import IntEnum

class ColumnEnum(IntEnum):
    NAME_COLUMN = 0
    YEAR_GROUP_COLUMN = 1
    TUTOR_GROUP_COLUMN = 2
    COLUMNS_BEFORE_EXAM_DATA = 3# 3 is the column where the exam data starts, before that is name,year_group and tutor_group

class FirstFieldEnum():
    HEADER_ROW = "Full Name"
    DEPARTMENT_ROW = "Department"
    TIMING_ROW = "Exam Length"
    ROOM_ROW = "Room"

