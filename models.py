
from dataclasses import dataclass, field
from datetime import date as Date
from enum import Enum
from typing import List


class CarType(str, Enum):
    PRIVATE = "Private"
    TRUCK = "Truck"
    BUS = "Bus"


@dataclass(frozen=True)
class RadarObservation:
    plate_number: str
    date: Date
    car_type: CarType
    speed: float
    seatbelt_fastened: bool


@dataclass(frozen=True)
class Violation:
    description: str
    fee: float
    rule_name: str 


@dataclass
class Fine:

    plate_number: str
    date: Date
    violations: List[Violation] = field(default_factory=list)

    @property
    def total_amount(self) -> float:
        return sum(v.fee for v in self.violations)

    def print_fine(self) -> None:
        print(f"Traffic for car {self.plate_number}")
        print(f"Total amount: {int(self.total_amount)} EGP")
        print("Violations:")
        for v in self.violations:
            print(f"- {v.description} : {int(v.fee)} EGP")