from django.db import models
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return f"{self.name}"


class Car(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True)

    MPG = 'MPG'
    LP100KM = 'LP100KM'
    GP100KM = 'GP100KM'
    KPG = 'KPG'
    FUEL_USAGE_CALC_MODE_CHOICES = [
        (MPG, 'Miles per gallon'),
        (LP100KM, 'Litres per 100 km'),
        (KPG, 'Kilometers per gallon'),
        (GP100KM, 'Gallons per 100 km'),
    ]
    fuel_usage_calc_mode = models.CharField(
        max_length=7,
        choices=FUEL_USAGE_CALC_MODE_CHOICES,
        default=LP100KM,
    )

    KM = 'KM'
    MILES = 'MI'
    DISTANCE_UNIT_CHOICES = [
        (KM, 'kilometers'),
        (MILES, 'miles'),
    ]
    distance_unit = models.CharField(
        max_length=2,
        choices=DISTANCE_UNIT_CHOICES,
        default=KM,
    )

    LITRES = 'LTR'
    GALLONS = 'GAL'
    FUEL_QUANTITY_UNIT_CHOICES = [
        (LITRES, 'litres'),
        (GALLONS, 'gallons'),
    ]
    fuel_quantity_unit = models.CharField(
        max_length=3,
        choices=FUEL_QUANTITY_UNIT_CHOICES,
        default=LITRES,
    )

    name = models.CharField(max_length=200)
    license_plate = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.license_plate})"


class Fill(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    odometer = models.IntegerField(default=0)
    unit_price = models.DecimalField(
        default=0.0, max_digits=10, decimal_places=3)
    amount_filled = models.DecimalField(
        default=0.0, max_digits=10, decimal_places=2)
    tank_full = models.BooleanField(default=True)
    fill_datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.fill_datetime}: {self.odometer}, {self.amount_filled} [{self.car}]"
