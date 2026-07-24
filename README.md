# Quantum Radar

A rule-based traffic radar system implemented in Python.

## Features

* Processes radar observations:

  * Plate number
  * Date
  * Vehicle type
  * Speed
  * Seatbelt status
* Generates zero or more violations per observation.
* Creates fines with total amount calculation.
* Provides:

  * `getAllPossibleFines()`
  * Violation statistics per rule.
* Fully extensible through independent rule classes (Open/Closed Principle).

## AI Model

Rule-Based Expert System.

## Project Structure

```text
main.py        # Demonstration
models.py      # Shared data models
rules.py       # Traffic rules
qu_radar.py    # Core radar logic
```

## Example Output

```text
Traffic for car ABC1234
Total amount: 400 EGP
Violations:
- Seatbelt not fastened : 100 EGP
- speed of 94 exceeded max allowed 80 : 300 EGP
```

## Run

```bash
python main.py
```
