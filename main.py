from datetime import date
from models import CarType, RadarObservation
from qu_radar import QuRadar
from rules import CarType 
from rules import TrafficRule
from models import Violation
from typing import Optional


def print_section(title: str) -> None:
    print()
    print(f"===== {title} =====")


def main() -> None:
    radar = QuRadar() 

    observations = [
        # Matches the exact example from the spec: speeding + no seatbelt.
        RadarObservation("ABC1234", date(2026, 7, 24), CarType.PRIVATE, 94, False),
        # Clean private car: no violation expected.
        RadarObservation("XYZ777", date(2026, 7, 24), CarType.PRIVATE, 70, True),
        # Truck speeding only.
        RadarObservation("TRK555", date(2026, 7, 24), CarType.TRUCK, 75, True),
        # Bus with unfastened seatbelt only.
        RadarObservation("BUS009", date(2026, 7, 24), CarType.BUS, 65, False),
        # Same private car speeding again on a later date.
        RadarObservation("ABC1234", date(2026, 7, 25), CarType.PRIVATE, 90, True),
    ]

    print_section("Processing observations")
    for obs in observations:
        fine = radar.process(obs)
        if fine is not None:
            fine.print_fine()
            print()
        else:
            print(f"No violation for car {obs.plate_number}")
            print()

    print_section("getAllPossibleFines (plate -> total amount)")
    for plate, total in radar.getAllPossibleFines().items():
        print(f"{plate}: {int(total)} EGP")

    print_section("Violation counts per rule")
    for rule_name, count in radar.get_violation_counts().items():
        print(f"{rule_name}: {count}")

    class MinimumSpeedRule(TrafficRule):
        FEE = 150

        def __init__(self, min_speed: float):
            self.min_speed = min_speed

        @property
        def name(self) -> str:
            return "minimum_speed"

        def check(self, observation: RadarObservation) -> Optional[Violation]:
            if observation.speed < self.min_speed:
                description = (
                    f"speed of {int(observation.speed)} below "
                    f"minimum required {int(self.min_speed)}"
                )
                return Violation(description=description, fee=self.FEE, rule_name=self.name)
            return None

    radar.add_rule(MinimumSpeedRule(min_speed=30))

    print_section("Extensibility check: new rule applied without touching QuRadar")
    slow_car = RadarObservation("SLW111", date(2026, 7, 26), CarType.PRIVATE, 15, True)
    fine = radar.process(slow_car)
    if fine is not None:
        fine.print_fine()


if __name__ == "__main__":
    main()