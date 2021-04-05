#! /usr/bin/env python3

import numpy as np
import pandas as pd
import random
import matplotlib.pyplot as plt
import scipy.stats as stats

mondays = pd.date_range(start=str(2011), end=str(2021), freq="W-MON").tolist()
thursdays = pd.date_range(start=str(2011), end=str(2021), freq="W-THU").tolist()
samplingDays = mondays + thursdays

grp1_3 = [1, 2, 3]
grp4_6 = [4, 5, 6]
grp7_9 = [7, 8, 9]
grp10_12 = [10, 11, 12]
grp13_15 = [13, 14, 15]
grp16_18 = [16, 17, 18]
grp19_21 = [19, 20, 21]
grp22_24 = [22, 23, 24]
grp25_27 = [25, 26, 27]
grp28_30 = [28, 29, 30]
grp31_33 = [31, 32, 33]
grp34_36 = [34, 35, 36]
grp37_39 = [37, 38, 39]
grp40_42 = [40, 41, 42]
grp43_45 = [43, 44, 45]
grp46_48 = [46, 47, 48]

disturbed = [grp1_3, grp4_6, grp7_9, grp10_12]
stream = [grp13_15, grp16_18, grp19_21, grp22_24]
forest = [grp37_39, grp40_42, grp43_45, grp46_48]
grass = [grp25_27, grp28_30, grp31_33, grp34_36]

habitatTypes = [
    dict(name="disturbed", boards=disturbed),
    dict(name="stream", boards=stream),
    dict(name="forest", boards=forest),
    dict(name="grass", boards=grass)
]

year = [2021, 2020, 2019, 2018, 2017, 2016, 2015, 2014, 2013, 2012, 2011]
months = list(range(1,13))
minTemp = [35, 38, 45, 51, 60, 67, 70, 70, 65, 53, 44, 38]
maxTemp = [56, 60, 68, 75, 82, 87, 90, 89, 84, 75, 66, 58]
meanTemp = [46, 49, 56, 63, 71, 77, 80, 79, 75, 64, 55, 48]

meanHumidity = .68
maxHumidity = 1.0
minHumidity = .20

# abund: relative abundance during each month of year
# habitatPref: relative preference for disturbed, stream, forest, or grass habitat
# svl: min, max, mean, standard deviation of snout vent length in mm
species = [
    dict(
        name="Pantherophis spiloides",
        abund=[0, 0, 5, 20, 18, 8, 5, 10, 8, 8, 0, 0],
        habitatPref=[3, 1, 5, 2],
        svl=[1, 100, 10, 2]
        ),
    dict(
        name="Coluber constrictor",
        abund=[0, 0, 5, 20, 25, 10, 5, 3, 10, 15, 0, 0],
        habitatPref=[2, 0, 1, 10],
        svl=[1, 100, 10, 2]
        ),
    dict(
        name="Eurycea cirrigera",
        abund=[20, 40, 30, 10, 5, 0, 0, 0, 0, 10, 25, 27],
        habitatPref=[0, 10, 1, 0],
        svl=[1, 100, 10, 2]
        ),
    dict(
        name="Plethodon glutinosus",
        abund=[30, 40, 15, 5, 0, 0, 0, 0, 0, 10, 18, 20],
        habitatPref=[10, 3, 5, 0],
        svl=[1, 100, 10, 2]
    ),
    dict(
        name="Storeria occipitomaculata",
        abund=[0, 2, 19, 21, 3, 4, 1, 0, 15, 12, 0, 0],
        habitatPref=[8, 0, 6, 3],
        svl=[1, 100, 10, 2]
        ),
    dict(
        name="Tantilla coronata",
        abund=[0,2,5,10,10,2,2,2,5,5,1,1],
        habitatPref=[2,0,1,0],
        svl=[1, 100, 10, 2]
    ),
    dict(
        name="Gastrophyne carolinensis",
        abund=[0,0,0,0,1,1,1,1,0,0,0,0],
        habitatPref=[1,1,1,1],
        svl=[1, 100, 10, 2]
    ),
    dict(
        name="Anaxyrus fowleri",
        abund=[0, 0, 15, 20, 18, 10, 5, 3, 8, 10, 3, 1],
        habitatPref=[5, 10, 3, 0],
        svl=[1, 100, 10, 2]
        ),
    dict(
        name="Anolis carolinensis",
        abund=[1, 2, 20, 65, 70, 55, 45, 50, 55, 40, 20, 15],
        habitatPref=[10, 1, 4, 1],
        svl=[1, 100, 10, 2]
        ),
    dict(
        name="Sceloporus undulatus",
        abund=[0, 10, 35, 40, 25, 20, 20, 50, 55, 45, 5, 0],
        habitatPref=[10, 0, 2, 0],
        svl=[1, 100, 10, 2]
        ),
    dict(
        name="Plestiodon fasciata",
        abund=[0, 15, 40, 75, 60, 20, 30, 40, 50, 35, 10, 0],
        habitatPref=[5, 0, 5, 0],
        svl=[1, 100, 10, 2]
        ),
    dict(
        name="Plestiodon laticeps",
        abund=[0, 4, 17, 22, 20, 15, 12, 10, 15, 10, 5, 0],
        habitatPref=[4, 0, 6, 0],
        svl=[1, 100, 10, 2]
        ),
    dict(
        name="Agkistrodon piscivorus",
        abund=[0, 0, 5, 10, 8, 0, 0, 10, 5, 0, 0, 0],
        habitatPref=[0, 10, 0, 0],
        svl=[1, 100, 10, 2]
        ),
    dict(
        name="Crotalus horridus",
        abund=[0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        habitatPref=[1, 0, 1, 0],
        svl=[1, 100, 10, 2]
        ),
    dict(
        name="Storeria dekayi",
        abund=[0, 2, 19, 21, 3, 4, 1, 0, 15, 12, 0, 0],
        habitatPref=[8, 2, 6, 3],
        svl=[1, 100, 10, 2]
        ),
     dict(
        name="Scincella lateralis",
        abund=[1, 2, 20, 80, 100, 75, 60, 60, 65, 50, 30, 10],
        habitatPref=[5, 3, 10, 1],
        svl=[1, 100, 10, 2]
        )   
] 

# Calculate monthly proportion from abundances
monthlyRelSpProbs = []
for mon in range(0, len(months)):
    totalAbund = 0 
    for sp in species:
        totalAbund += sp["abund"][mon]
    relSpProbs = []
    for sp in species:
        relSpProbs.append(sp["abund"][mon] / totalAbund)
    monthlyRelSpProbs.append(relSpProbs)

# Calculate proportion of habitat preferences
for sp in species:
    total = sum(sp["habitatPref"])
    sp["habitatPrefWeight"] = [i/total for i in sp["habitatPref"]]

observations = []
for day in samplingDays:
    month = day.month
    temperature = random.uniform(minTemp[month - 1], maxTemp[month - 1])
    humidity = random.uniform(minHumidity, maxHumidity) 
    if temperature < 50:
        tempScore = 1
    elif temperature > 50 < 60:
        tempScore = 2
    elif temperature > 60 < 75:
        tempScore = 3
    elif temperature > 75:
        tempScore = 4
    else:
        quit("Invalid temperature: {}".format(temperature))

    if humidity < 0.5:
        humidScore = 1
    elif humidity > 0.5:
        humidScore = 2
    else:
        quit("Invalid humidity: {}".format(humidity))

    totalScore = tempScore + humidScore 
    numberOfObservations = np.random.poisson(lam=totalScore - 0.5)
    
    for i in range(numberOfObservations):
        spEntry = random.choices(species, weights=monthlyRelSpProbs[month - 1], k=1)[0]
        habitat = random.choices(habitatTypes, weights=spEntry["habitatPrefWeight"], k=1)[0]
        habitatGrp = random.choice(habitat["boards"])  
        boardNum = random.choice(habitatGrp)

        # Get random svl from truncated lognormal
        svlParams = spEntry["svl"]
        lower, upper = np.log(svlParams[0]), np.log(svlParams[1]) 
        mu, sigma = np.log(svlParams[2]), np.log(svlParams[3]) 
        model = stats.truncnorm(
            (lower - mu) / sigma, (upper - mu) / sigma, loc=mu, scale=sigma)
        svl = round(np.exp(model.rvs(1))[0])

        # Append data
        observations.append({
            "date": day.strftime("%Y-%m-%d"),
            "species": spEntry["name"],
            "svl (mm)": svl,
            "board number": boardNum,
            "habitat type": habitat["name"],
            "air temp (degrees Fahrenheit)": round(temperature, 1),
            "relative humidity (percent)": round(humidity, 3),
        })


df = pd.DataFrame.from_dict(observations)
df.sort_values("date")
df.to_csv("herp_proj_data.csv", index=False)
