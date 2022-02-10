import enum


class Product(enum.Enum):
    P1 = 1
    P2 = 2
    P3 = 3


class Component(enum.Enum):
    C1 = 1
    C2 = 2
    C3 = 3


class Event_Types(enum.Enum):
    Inspection_Complete = 1
    Add_to_Buffer = 2
    Unbuffer_Start_Assembly = 3
    Assembly_Complete = 4
