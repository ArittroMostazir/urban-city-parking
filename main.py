from abc import ABC, abstractmethod
from datetime import datetime



class Vehicle(ABC):
    def __init__(self, plate_number):
        self.plate_number = plate_number

    @abstractmethod
    def get_rate(self):
        pass


class PricingStrategy(ABC):
    @abstractmethod
    def calculate_fee(self, hours, rate):
        pass




class Car(Vehicle):
    def get_rate(self):
        return 7


class Bike(Vehicle):
    def get_rate(self):
        return 3


class Truck(Vehicle):
    def get_rate(self):
        return 10




class PeakPricing(PricingStrategy):
    def calculate_fee(self, hours, rate):
        return hours * rate * 1.5


class OffPeakPricing(PricingStrategy):
    def calculate_fee(self, hours, rate):
        return hours * rate


class WeekendPricing(PricingStrategy):
    def calculate_fee(self, hours, rate):
        return hours * rate * 1.2




class ParkingTicket:
    def __init__(self, vehicle, pricing_strategy):
        self.vehicle = vehicle
        self.pricing_strategy = pricing_strategy
        self.entry_time = datetime.now()
        self.exit_time = None

    def close_ticket(self):
        self.exit_time = datetime.now()

    def calculate_duration(self):
        duration = self.exit_time - self.entry_time
        return max(1, duration.seconds // 3600)

    def calculate_fee(self):
        hours = self.calculate_duration()
        rate = self.vehicle.get_rate()
        return self.pricing_strategy.calculate_fee(hours, rate)




class ParkingLot:
    def __init__(self, capacity=300):
        self.capacity = capacity
        self.available_spaces = capacity
        self.active_tickets = {}

    def park_vehicle(self, vehicle, pricing_strategy):
        if self.available_spaces <= 0:
            print("Parking lot is full.")
            return None

        ticket = ParkingTicket(vehicle, pricing_strategy)
        self.active_tickets[vehicle.plate_number] = ticket
        self.available_spaces -= 1
        print(f"Vehicle {vehicle.plate_number} parked.")
        return ticket

    def exit_vehicle(self, plate_number):
        ticket = self.active_tickets.get(plate_number)
        if not ticket:
            print("Vehicle not found.")
            return

        ticket.close_ticket()
        fee = ticket.calculate_fee()
        self.available_spaces += 1
        del self.active_tickets[plate_number]

        print(f"Vehicle {plate_number} exited.")
        print(f"Parking Fee: ${fee}")




if __name__ == "__main__":
    parking_lot = ParkingLot()

    vehicle = Car("1234")
    pricing = OffPeakPricing()

    ticket = parking_lot.park_vehicle(vehicle, pricing)

    # Simulate exit
    parking_lot.exit_vehicle("1234")

