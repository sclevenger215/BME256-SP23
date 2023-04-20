import numpy as np

#Importing initial values
alpha = 0.99
nsteps = 2000 #Number of incrementations
bigN = 500 #Number of velocity values to generate
deltaP = 1333 #dynes/cm^2
mu = 0.035 #dyne-sec/cm^2
vseed = 20 #cm/sec

#Initial artery size
r2 = 0.3 #cm
r1 = 0 #cm
L = 5 #cm

dr = r2 / bigN #cm

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
for o in range(0, bigN): #Calaulates the volumetric flow
    Ftot += 2 * np.pi * o * dr ** 2 * v[o]
print(f'The total flow is {Ftot} cm^3/s')

print(f'The experimental resistance is {deltaP / Ftot} Ohms')

#Calculates the theoretical axial flow
Q = np.pi * deltaP * r2**4 / (8 * mu * L)
print(f'The theoretical flow is {Q} cm^3/sec')

deltaPQ = deltaP / Q
print(f'The theoretical resistance is {deltaPQ} Ohms')
