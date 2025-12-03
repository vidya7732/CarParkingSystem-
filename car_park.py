from pathlib import Path
from datetime import datetime
from sensor import Sensor
from display import Display
import json

class CarPark:
    # Initialize the CarPark with location, capacity, and optional lists for plates, displays, and log file
    def __init__(self, location, capacity, plates=None, displays=None, log_file=Path("log.txt")):
        self.location = location
        self.capacity = capacity
        self.plates = plates or []  # List of license plates, initialized empty if None
        self.displays = displays or []  # List of Display objects, initialized empty if None
        self.log_file = log_file if isinstance(log_file, Path) else Path(log_file)  # Ensure log_file is a Path object
        self.log_file.touch(exist_ok=True)  # Create log file if it doesn't exist

    # String representation of the CarPark for printing
    def __str__(self):
        return f"Car park at {self.location}, with {self.capacity} bays."

    # Register a Sensor or Display object with the CarPark
    def register(self, component):
        if not isinstance(component, (Sensor, Display)):
            raise TypeError("Object must be a Sensor or Display")
        if isinstance(component, Display):
            self.displays.append(component)

    # Property to calculate available bays, ensuring it doesn't go negative
    @property
    def available_bays(self):
        return max(0, self.capacity - len(self.plates))

    # Update all registered displays with current status
    def update_displays(self):
        data = {"available_bays": self.available_bays, "temperature": 25}  # Sample temperature data
        for display in self.displays:
            display.update(data)

    # Add a car to the park and log the entry
    def add_car(self, plate):
        self.plates.append(plate)
        self.update_displays()
        self._log_car_activity(plate, "entered")

    # Remove a car from the park and log the exit
    def remove_car(self, plate):
        if plate in self.plates:  # Check if plate exists to avoid ValueError
            self.plates.remove(plate)
            self.update_displays()
            self._log_car_activity(plate, "exited")

    # Private method to log car activity with timestamp
    def _log_car_activity(self, plate, action):
        with self.log_file.open("a") as f:
            f.write(f"{plate} {action} at {datetime.now():%Y-%m-%d %H:%M:%S}\n")

    # Write car park configuration to a JSON file
    def write_config(self):
        with open("config.json", "w") as f:
            json.dump({"location": self.location, "capacity": self.capacity, "log_file": str(self.log_file)}, f)

    # Class method to create a CarPark instance from a config file
    @classmethod
    def from_config(cls, config_file=Path("config.json")):
        config_file = config_file if isinstance(config_file, Path) else Path(config_file)
        with config_file.open() as f:
            config = json.load(f)
        return cls(config["location"], config["capacity"], log_file=config["log_file"])