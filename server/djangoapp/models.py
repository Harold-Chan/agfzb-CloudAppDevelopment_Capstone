from django.db import models
from django.utils.timezone import now
from datetime import datetime

# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null=False, max_length=50)
    description = models.TextField(max_length=200)

    def __str__(self):
        return f"Car Make: {self.name}, Description: {self.description}"


# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car model object
class CarModel(models.Model):
    name = models.CharField(null=False, max_length=30)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id = models.IntegerField()
    TYPE_CHOICES = [
        ('hatchback', 'Hatchback'), ('suv', 'SUV'), ('saloon', 'Saloon'),
        ('estate', 'Estate'), ('coupe', 'Coupe'), ('convertible', 'Convertible'),
        ('pick_up', 'Pick Up')
    ]
    car_type = models.CharField(null=False, max_length=20, choices=TYPE_CHOICES, default='hatchback')
    YEAR_CHOICES = [(year, year) for year in range(datetime.now().year, 1949, -1)]
    year = models.IntegerField(choices=YEAR_CHOICES)

    def __str__(self):
        return f"Car Model: {self.name}, Make: {self.car_make}, Type: {self.car_type}, Year: {self.year}"

# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state short form
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, review, purchase=False, purchase_date="n/a", car_make="n/a", car_model="n/a", car_year="n/a", sentiment="n/a", id=None):
        # Dealer ID for the related dealer
        self.dealership = dealership
        # Reviewer Name
        self.name = name
        # User's review
        self.review = review
        # Purchase decision, boolean true/false
        self.purchase = purchase
        # Purchase Date
        self.purchase_date = purchase_date
        # Car Make
        self.car_make = car_make
        # Car Model
        self.car_model = car_model
        # Car Year
        self.car_year = car_year
        # Sentiment (positive, neutral, negative)
        self.sentiment = sentiment
        # Unique ID (optional, can be None)
        self.id = id

    def __str__(self):
        return f"Review for {self.dealership.full_name} by {self.name}"
