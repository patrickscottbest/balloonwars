from ambiance import Atmosphere
import matplotlib.pyplot as plt
import pandas as pd
pd.set_option('display.max_rows', None)


''' BalloonWars 

A python program to calculate the scientific parameters of launching of a totally-not-a-spy weather balloon.
'''


def reynolds_pipe(density, velocity, diameter, viscosity):
    """
    Calculate the Reynolds number for a given pipe flow.
    The resulting Reynolds number is dimensionless. 
    It is used to characterize flow patterns.

    Arguments:
    density -- density of the fluid in [kg/m3]
    velocity -- the mean velocity of the fluid in [m/s]
    viscosity -- dynamic viscosity of the fluid in [Pa*s]
    diameter -- inside diameter of the pipe in [m]
    """
    return density * velocity * diameter / viscosity
pi = 3.1415926535897931


diameter = (0.471921 * 2) #  metres, 0.471921 radius , 0.421921 cubic meter 14.9 ft3
volume = float(4.0/3.0*pi* (diameter/2)**3)
helium_mass = 0.166 * volume #  0.166 per m^3
payload = 0.50 #  kg
balloon = 0.2 #  kg
mass = helium_mass + balloon + payload  # kg 
print("-------------------------------------")
print("Initial_Displace(m^3): ", volume, "\nDiameter(m): ", diameter, "\nHelium(kg)", helium_mass, "\nMass(kg):", mass)

# User defined, generally a sphere standin is used in the laminar at low Reynolds
CoD = 0.4 # static for now.  0.4 sphere at any turbulent. 0.014 naca airfoils, symmetrical at Re 100,000

# User defined.
alt_m_low = 0
alt_m_high = 10000  # metres
stop_height = alt_m_high

# Initialise values
altitude = 0  # in metres
pressure = Atmosphere(altitude).pressure[0]
temp = Atmosphere(altitude).temperature[0]
time = 0
mycurrentspeed = 0


print("Stop height(m): ",stop_height)

launch = True
plot_time=[]
plot_altitude=[]

datum_headers = ["Time(s)", 
    "Alt(m)",
    "Speed((m/s)",
    "AtmosPress(pasc)",
    "AtmosTemp(C)",
    "AtmosDensity(kg/m^3)",
    "BalloonVolume",
    "BalloonDiameter",
    "ReNumber",
    "Buoyancy(N)",
    "Drag(N)",
    "Uplift(N)",
    "Acceleration Period(m/s)",
    "dynamic_viscosity",
    "kinematic_viscosity(m^2/s)",  # N s/m2, Pa s or kg/(m s)
    "grav_accel",
    "SpeedSound(m/s)",
    "MachNumber"
    ]
datum = []

while altitude < stop_height: 
    
    ## using previous values
    previous_pressure = pressure 
    previous_temp = temp 
    previous_diameter = diameter

    time += 1
    temp = Atmosphere(altitude).temperature[0]
    pressure = Atmosphere(altitude).pressure[0]

    new_volume = volume * (previous_pressure / pressure)  # V_2 = V_1 * (P_1 / P_2)
    volume = new_volume 
    diameter = (3*volume / 4*pi )**(1/3)  # (3V / (4π))^(1/3)
    
    airdensity = Atmosphere(altitude).density[0]
    grav_accel  = Atmosphere(altitude).grav_accel[0]
    temp_celsius = Atmosphere(altitude).temperature_in_celsius[0]

    drag =  CoD * airdensity * diameter / 2
    buoyancy =  volume * airdensity   # Newtons
    
    #uplift = (buoyancy - drag) * grav_accel  # UT=\rho_{air}BVg
    uplift = (buoyancy - drag)   # UT=\rho_{air}BVg
    # does not include gravity ?  uplift = buoyancy - drag - (Atmosphere(altitude).grav_accel * mass)
    accel_period = uplift/mass # f=m*a
    mycurrentspeed = accel_period
    altitude += mycurrentspeed
    
    dynamic_viscosity = Atmosphere(altitude).dynamic_viscosity[0]
    kinematic_viscosity = Atmosphere(altitude).kinematic_viscosity[0]
    re_number = int(reynolds_pipe(airdensity, mycurrentspeed, diameter, (dynamic_viscosity*9.80665)))  # need it in pascal/s

    #unused at the moment
    speed_of_sound = Atmosphere(altitude).speed_of_sound[0]
    mach = mycurrentspeed / (speed_of_sound)

    datum.append([time, 
        altitude,
        mycurrentspeed,
        pressure,
        temp_celsius,
        airdensity,
        volume,
        diameter,
        re_number,
        buoyancy,
        drag,
        uplift,
        accel_period,
        dynamic_viscosity,
        kinematic_viscosity, 
        grav_accel,
        speed_of_sound,
        mach
        ]
        )

    if (altitude < -1):
        print("----------------------------SINKING")
        quit()
    if (mycurrentspeed <= 0):
        print("----------------------------Maximum Altitude")
        break

dataframe = pd.DataFrame(datum, columns = datum_headers)
print(dataframe.head())
print(dataframe.tail())

dataframe.plot(subplots=True, y=datum_headers, secondary_y="Drag(N)", kind="line", figsize=(15,15), title=("Balloon Ascent to " + str(stop_height) +"m."), xlabel="Time(s)", layout=(4,5))

#dataframe.plot(y=["Buoyancy(N)","Uplift(N)","Drag(N)"], secondary_y="Drag(N)", kind="line", figsize=(5,5), title="Force Newtons", xlabel="Time(s)")
dataframe.plot(subplots=True, y=["Buoyancy(N)","Uplift(N)","Drag(N)"], kind="line", figsize=(5,5), title="Force Newtons", xlabel="Time(s)")

dataframe.plot(y="ReNumber", kind="line", figsize=(5,5), title="Reynolds Domain (log)", xlabel="Time(s)", logy=True)

plt.show()

quit()