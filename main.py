from car_park import CarPark
from sensor import EntrySensor, ExitSensor
from display import Display


def main():
    # Create a new CarPark instance with Moondalup location and capacity of 100, using a custom log file
    car_park = CarPark("Moondalup", 100, log_file="moondalup.txt")

    # Write the current configuration to a JSON file
    car_park.write_config()

    # Reinitialize the CarPark from the config file to demonstrate config loading
    car_park = CarPark.from_config("config.json")

    # Create an EntrySensor to detect cars entering the car park
    entry_sensor = EntrySensor(1, True, car_park)

    # Create an ExitSensor to detect cars leaving the car park
    exit_sensor = ExitSensor(2, True, car_park)

    # Create a Display to show parking information and register it with the CarPark
    display = Display(1, "Welcome to Moondalup", True)
    car_park.register(display)

    # Simulate 10 cars entering the car park using the entry sensor
    print("Simulating 10 cars entering...")
    for _ in range(10):
        entry_sensor.detect_vehicle()

    # Simulate 2 cars exiting the car park using the exit sensor
    print("\nSimulating 2 cars exiting...")
    for _ in range(2):
        exit_sensor.detect_vehicle()


if __name__ == "__main__":
    main()