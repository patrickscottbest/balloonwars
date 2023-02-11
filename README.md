# BalloonWars 

A python program to calculate the scientific parameters of launching of a totally-not-for-spying weather balloon.

![BalloonWars Logo](logo/png/logo-color.png?raw=true "BalloonWars Logo")

# Introduction

I decided to write a function to calculate a second by second launch of a weather balloon to a given altitude, and to produce a graphical output of it's journey.

The purpose was to explore what differences different parameters can make, and to understand the regimes of the atmosphere in which these balloons operate.  Neat.

# How to Run

Download the source code and run manually from the command line, any OS: 
```
python3 ./balloonwars.py --help
```

# What's missing? 

Lots.  

- Pressure of balloon compression
- Effects of temperature absorbtion
- Burst heigh calculations (material science i guess)
- Any kind of lat/long prediction or descent profile (post-burst)
- Reasonable documentation

# Resources and Research

Most published results show the coefficient of drag for a sphere at Re=10,000 to
be at or near 0.4. From there Cd increases to a broad maximum between 0.45 and 0.50
around Re=100,000 (Figure 2). As the curve continues, it drops off again as critical
turbulence is reached at Re ~ 200,000. The simulation results in this study show Cd
decreasing slightly between Re=10,000 and Re=100,000

The C_{dr} CoD should be considered a function of Re and practically of altitude. 
In our model we will set the drag coefficient at 0.47; 
that will be a value too high for ground conditions and far more appropriate for low Re high altitude conditions
https://www.basicairdata.eu/knowledge-center/design/introduction-to-weather-balloons/

REASONABLE SANITY NUMBERS    
-pressure_sealevel_kp = 1013.25
-pressure_ceiling_kp = 10 
-sound_m_s_high = 340
-sound_m_s_low = 200