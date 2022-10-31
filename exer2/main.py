from simpful import *
"""
Mateusz Miekicki s20691
Oskar Przydatek s19388

Program helps to determine the acceleration value for a vehicle taking into account 
parameters such as predxc, mass and distance to the nearest obstacle.
The program takes three numeric variables such as
  - Speed
  - Distance
  - Weight

The solution uses the Mandami algorithm to interpret linguistic variables.
"""

FS = FuzzySystem()

speed_slow = FuzzySet(function=Triangular_MF(a=10, b=37, c=50), term="slow")
speed_medium = FuzzySet(function=Triangular_MF(
    a=35, b=52, c=73), term="medium")
speed_high = FuzzySet(function=Triangular_MF(a=45, b=78, c=94), term="high")
LV1 = LinguisticVariable(
    [speed_slow, speed_medium, speed_high], concept="Speed",
    universe_of_discourse=[10, 94])
FS.add_linguistic_variable("Speed", LV1)
"""
Linguistic variable responsible for interpretation of speed in three levels
"""

distance_short = FuzzySet(function=Triangular_MF(
    a=2, b=15, c=23), term="short")
distance_medium = FuzzySet(function=Triangular_MF(
    a=10, b=25, c=37), term="medium")
distance_long = FuzzySet(function=Triangular_MF(
    a=33, b=50, c=70), term="long")
LV2 = LinguisticVariable(
    [distance_short, distance_medium, distance_long], concept="Distance",
    universe_of_discourse=[2, 70])
FS.add_linguistic_variable("Distance", LV2)
"""
Linguistic variable responsible for interpretation of distance in three levels
"""

weight_small = FuzzySet(function=Triangular_MF(
    a=1000, b=1350, c=1700), term="samll")
weight_medium = FuzzySet(function=Triangular_MF(
    a=1450, b=1800, c=2300), term="medium")
weight_big = FuzzySet(function=Triangular_MF(
    a=2000, b=2450, c=2700), term="big")
LV4 = LinguisticVariable(
    [weight_small, weight_medium, weight_big], concept="Weight",
    universe_of_discourse=[1000, 2700])
FS.add_linguistic_variable("Weight", LV4)
"""
Linguistic variable responsible for the interpretation of the weight in three levels
"""

acceleration_big_minus = FuzzySet(function=Triangular_MF(
    a=-1., b=-.7, c=-0.5), term="big_minus")
acceleration_small_minus = FuzzySet(function=Triangular_MF(
    a=-.6, b=-.3, c=0.), term="small_minus")
acceleration_small_plus = FuzzySet(function=Triangular_MF(
    a=0, b=0.1, c=0.4), term="small_plus")
acceleration_big_plus = FuzzySet(function=Triangular_MF(
    a=0.3, b=.7, c=1), term="big_plus")
LV3 = LinguisticVariable(
    [acceleration_big_minus, acceleration_small_minus,
        acceleration_small_plus, acceleration_big_plus],
    concept="Acceleration", universe_of_discourse=[-1, 1])
FS.add_linguistic_variable("Acceleration", LV3)
"""
The linguistic variable responsible for the interpretation of the above three inputs
"""

FS.add_rules_from_file(path='list_of_rules.txt')
"""
Upload list of rules from an file
"""

FS.set_variable("Speed", 80)
FS.set_variable("Distance", 10)
FS.set_variable("Weight", 1800)

print(FS.Mamdani_inference(["Acceleration"]))