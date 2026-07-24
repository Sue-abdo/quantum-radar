from abc import ABC, abstractmethod
from typing import Dict, Optional
from models import CarType, RadarObservation, Violation

class TrafficRule(ABC):
    @property
    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def check(self, observation: RadarObservation) -> Optional[Violation]:

        raise NotImplementedError


class SpeedLimitRule(TrafficRule):

    FEE = 300 

    def __init__(self, car_type: CarType, max_speed: float):
        self.car_type = car_type
        self.max_speed = max_speed

    @property
    def name(self) -> str:
        return f"speed_limit_{self.car_type.value.lower()}"

    def check(self, observation: RadarObservation) -> Optional[Violation]:
        if observation.car_type != self.car_type:
            return None
        if observation.speed > self.max_speed:
            description = (
                f"speed of {int(observation.speed)} exceeded "
                f"max allowed {int(self.max_speed)}"
            )
            return Violation(description=description, fee=self.FEE, rule_name=self.name)
        return None


class SeatbeltRule(TrafficRule):

    FEE = 100

    @property
    def name(self) -> str:
        return "seatbelt"

    def check(self, observation: RadarObservation) -> Optional[Violation]:
        if not observation.seatbelt_fastened:
            return Violation(
                description="Seatbelt not fastened",
                fee=self.FEE,
                rule_name=self.name,
            )
        return None


def default_rules() -> Dict[str, TrafficRule]:
    rules = [
        SeatbeltRule(),
        SpeedLimitRule(CarType.TRUCK, 60),
        SpeedLimitRule(CarType.PRIVATE, 80),
        SpeedLimitRule(CarType.BUS, 70),
    ]
    return {rule.name: rule for rule in rules}