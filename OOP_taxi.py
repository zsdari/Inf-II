#Taxis példa
import datetime
from functools import partial


class Taxi:

    old_taxi = 0
    new_taxi = 0

    def __init__(self, licence, km, next_service, partial_km, consumption, tank_l):
        self.licence = licence
        self.km = km
        self.next_service = next_service
        self.partial_km = partial_km
        self.consumption = consumption
        self.tank_l = tank_l
        if self.km > 100000:
            type(self).old_taxi += 1
        else:
            type(self).new_taxi += 1

    def km_left(self):
        return round((self.tank_l / self.consumption * 100) - self.partial_km, 2)

    def service(self):
        return self.next_service - datetime.datetime.now().year

    @classmethod
    def fleet_count(cls):
        return cls.old_taxi + cls.new_taxi
    @staticmethod
    def fleet_info():
        return "\t - Phone: +36 88 123 123\n\t - Email: taxi@python.hu"

taxi_fleet_tests = [
    {
        'licence': 'ABC-123',
        'km': 123456,
        'next_service': '2025-01-20',
        'partial_km': 567,
        'consumption': '9.2 L/100km',
        'tank_l': 60
    },
    {
        'licence': 'DEF-456',
        'km': 78901,
        'next_service': '2024-11-30',
        'partial_km': 89,
        'consumption': '7.8 L/100km',
        'tank_l': 50
    },
    {
        'licence': 'GHI-789',
        'km': 234567,
        'next_service': '2025-02-10',
        'partial_km': 432,
        'consumption': '10.1 L/100km',
        'tank_l': 65
    },
    {
        'licence': 'JKL-012',
        'km': 3456,
        'next_service': '2024-10-05',
        'partial_km': 12,
        'consumption': '6.5 L/100km',
        'tank_l': 45
    },
    {
        'licence': 'MNO-345',
        'km': 98765,
        'next_service': '2024-12-01',
        'partial_km': 345,
        'consumption': '8.9 L/100km',
        'tank_l': 55
    }
]

taxi_01 = Taxi('ABC123', 123456, 2027, 450, 8.5, 52)
taxi_02 = Taxi('ABC125', 13456, 2032, 10, 5.7, 45)
taxi_03 = Taxi('TGD678', 265486, 2028, 40, 11.4, 60)

print(taxi_01.service())
print(taxi_02.service())
print(taxi_03.km_left())
print(f'Uj jarmu db: {Taxi.new_taxi} \nRegi jarmu db: {Taxi.old_taxi}')
print(f'Jarmuvek osszesen: {Taxi.fleet_count()}')
print(f'Elerhetosegek:\n{Taxi.fleet_info()}')