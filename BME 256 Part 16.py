import matplotlib.pyplot as plt
import numpy as np

#Importing initial values
alpha = 0.99
nsteps = 2000 #Number of incrementations
bigN = 500 #Number of velocity values to generate
deltaP = 1333 #dynes/cm^2
mu = 0.035 #dyne-sec/cm^2
vseed = 20 #cm/sec

#Wire comparison artery size
radius = [0, 0.023, 0.018] #The no catheter, Volcano, and FloWire radii
L = 6 #cm

arteries = [0.25, 0.2, 0.15, 0.1, 0.05] #Artery radii to test

#Calculates the vascular downstream resistance
SPP = 126635 #dyne-sec/cm^2
TCO = 5 * 1000 / 60 #cm^3/sec
CCO = TCO * 0.1 #Calculates the percent of the cardiac output that goes through the coronary arteries
LAD = CCO / 3 #Calculate the portion of the coronary cardiac output that goes through the LAD

VolRatios = []
FloRatios = []
for r2 in arteries:    
    dr = r2 / bigN #cm
    R = [SPP/ LAD] #Creates a list to hold resistance values and adds the vascular downstream resistance
    for r1 in radius: #To calculate the flow with different catheter sizes
        v = np.zeros(bigN + 1) #Creating a vector to store values in
        v.fill(vseed) #Initializing the vector values to vseed
        v[bigN:] = 0
        for i in range(nsteps): #Incrementing nsteps times
            for n in range(bigN): #Calculating velocity for each node
                #Only calculating the velcoity if the radius is bigger than r1 and less than r2
                vlast = v[n] #Save the last iteration's value
                if r1 < dr: #Sets the first value equal to the second if r1 is less than dr
                    v[0] = v[1]
                if n * dr > r1 and n * dr < r2:
                    v[n] = 0.5 * (deltaP * dr**2 / mu / L + (1 + 0.5 / n) * v[n + 1] + (1 - 0.5 / n) * v[n - 1])
                else:
                    v[n] = 0
                v[n] = v[n] + alpha * (v[n] - vlast) #Adjust the velocity to the previous iteration
    
        #Calculates the axial flow based on model
        Ftot = 0 #Sets a placeholder value to calculate the flow
        for o in range(0, bigN): #Calculates the volumetric flow
            Ftot += 2 * np.pi * o * dr ** 2 * v[o]

        R.append(deltaP / Ftot) #Adds the resistance value to the resistance list

    #Calculates the flow ratios for each wire type
    R[0] -= R[1] #Calculates R2
    print(f'The artery radius is {r2}')
    print(f'R2 is {R[0]}')
    print(f'R1 is {R[1]}')
    print(f'Volcano R1 prime is {R[2]}')
    print(f'FloWire R1 prime is {R[3]}')
    
    Volcano = (R[1] + R[0]) / (R[2] + R[0]) #Calculates the flow ratio for Volcano wire
    VolRatios.append(Volcano) #Adds the flow ratio to the list
    print(f'The Volcano ratio for the artery radius of {r2} cm is {Volcano}')
    
    FloWire = (R[1] + R[0]) / (R[3] + R[0]) #Calculates the flow ratio for FloWire
    FloRatios.append(FloWire) #Adds the flow ratio to the list
    print(f'The FloWire ratio for the artery radius of {r2} cm is {FloWire}')
    
Ratios = [VolRatios, FloRatios] #Matrix to hold the flow ratios
titles = ['Volcano', 'FloWire'] #List to hold the plot titles
print(Ratios)
for c in range(len(Ratios)): #Plots the different wire ratios on different plots
    plt.plot(arteries, Ratios[c])
    plt.title(f'{titles[c]} Ratios')
    plt.xlabel('Radius (cm)')
    plt.ylabel('Flow Ratio')
    plt.show()
