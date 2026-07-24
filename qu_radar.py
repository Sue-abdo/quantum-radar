
from typing import Dict, List, Optional
from models import Fine, RadarObservation, Violation
from rules import TrafficRule, default_rules


class QuRadar:
    def __init__(self, rules: Optional[List[TrafficRule]] = None):
        self._rules: Dict[str, TrafficRule] = (
            {r.name: r for r in rules} if rules is not None else default_rules()
        )
        self._fines: List[Fine] = []
        self._violation_counts: Dict[str, int] = {}

    def add_rule(self, rule: TrafficRule) -> None:
        self._rules[rule.name] = rule

    def process(self, observation: RadarObservation) -> Optional[Fine]:
        violations: List[Violation] = []
        for rule in self._rules.values():
            violation = rule.check(observation)
            if violation is not None:
                violations.append(violation)
                self._violation_counts[violation.rule_name] = (
                    self._violation_counts.get(violation.rule_name, 0) + 1
                )

        if not violations:
            return None

        fine = Fine(
            plate_number=observation.plate_number,
            date=observation.date,
            violations=violations,
        )
        self._fines.append(fine)
        return fine

    def getAllPossibleFines(self) -> Dict[str, float]:
        totals: Dict[str, float] = {}
        for fine in self._fines:
            totals[fine.plate_number] = totals.get(fine.plate_number, 0) + fine.total_amount
        return totals

    def get_violation_counts(self) -> Dict[str, int]:
        return dict(self._violation_counts)

    def get_all_fines(self) -> List[Fine]:

        return list(self._fines)